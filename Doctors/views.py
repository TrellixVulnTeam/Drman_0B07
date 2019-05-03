from django.shortcuts import render, get_object_or_404, redirect
from .models import Loc_Category,Spec_Category, DoctorsPost , OpeningHours , QuestionView
from taggit.models import Tag
from django.db.models import Count
from django.views.generic import ListView
from django.views.generic.edit import FormView
from .forms import EmailPostForm , CommentsForm , SearchForm, FilterSearchForm , searchDetail , MapForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import quote_plus
from .search import DoctorsIndex
from django.shortcuts import render_to_response
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_protect
from django.utils.safestring import mark_safe
from django.template import Context
from django.http import HttpResponse
from django.core.urlresolvers import resolve
from django.views.generic.detail import DetailView
import datetime
import json

#TODO : can we optimize and don't copy these code from blog and inherit from it ?
#TODO : add all for select all in choices

def core_filter_search(query_brand,query_car ,query_specialty):
    es = Elasticsearch(['http://elasticsearch613:9200/'])
    # q = Q("multi_match", query=query_brand, fields=['title', 'text', 'loc_cat', 'spec_cat' , 'tags']) & Q("multi_match", query=query_car, fields=['title', 'text', 'loc_cat', 'spec_cat' , 'tags'])

    if query_specialty :
        q = Q("match", spec_cat=query_specialty)

    if query_brand :
        q = Q("match", loc_cat=query_brand)

    if query_car:
        q = Q("match", loc_cat = query_car)

    if query_brand and query_car :
        q = Q("match", loc_cat=query_brand) & Q("match", loc_cat=query_car)

    if query_brand and query_specialty :
        q = Q("match", loc_cat=query_brand) & Q("match", spec_cat = query_specialty)

    if query_car and query_specialty :
        q = Q("match", loc_cat = query_car) & Q("match", spec_cat = query_specialty)

    if query_brand and query_car and query_specialty :
        q = Q("match", loc_cat = query_brand) & Q("match", loc_cat = query_car) & Q("match", spec_cat = query_specialty)
    else:
        q = Q("match", loc_cat = "اصفهان") & Q("match", loc_cat = "حکیم نظامی") & Q("match", spec_cat = "گوهردشت")

    ss = Search(using=es, index='doctor').query(q)
    return ss

# ToDo : if we have
def core_search(query):
    es = Elasticsearch(['http://elasticsearch613:9200/'])
    q = Q("multi_match", query=query, fields=['title', 'text', 'loc_cat', 'spec_cat' , 'tags' ])

    ss = Search(using=es, index='doctor').query(q)
    return ss

# Add index doctor to kibana
# PUT doctor
# {
#     "mappings": {
#         "doc" : {
#             "properties" : {
#                 "title_suggest" : {
#                     "type" : "completion",
#                     "search_analyzer": "simple",
#                     "analyzer": "simple"
#                 },
#                 "title" : {
#                     "type": "text"
#                 }
#             }
#         }
#     }
# }

# ToDo: if we have not mapping index in kibana at first time , make it automatically
# ToDo: if we don't save any post , we get error in auto complete
def completion_suggester(request) :

    if request.POST:
        query = request.POST.get('search_text')
    else :
        query = ""

    ss = core_search(query)
    ss = ss.suggest(
        'title_suggestions',
        query,
        completion={
            'field': 'title_suggest',
            "skip_duplicates": True,
            "fuzzy": {
                "fuzziness": 2
            }
        })

    results = ss.execute()

    for result in results.suggest.title_suggestions:
        suggest = []
        for result_title in result.options:
            suggest.append(result_title['_source']['title'])

    mimetype = 'application/json'
    return HttpResponse(json.dumps(suggest), mimetype)
    # return render_to_response('doctors/post/ajax_search.html', {'doctors': suggest})



# @csrf_exempt
# def filter_search(request) :
#
#     query = request.GET.get("specialty","").strip()
#     query_state = request.GET.get("brand","").strip()
#     query_area = request.GET.get("car","").strip()
#     query_list = [query, query_state , query_area]
#     ss = core_filter_search(query_list)
#     results = ss.execute()
#     return render(request, 'doctors/post/test.html' , {'doctors': [hit for hit in results]  })

@csrf_exempt
def search(request) :

    query = request.GET.get("search","").strip()
    ss = core_search(query)
    results = ss.execute()
    return render(request, 'doctors/post/test.html' , {'doctors': [hit for hit in results]  })

@csrf_exempt
def multiple_forms(request):
    searchform = SearchForm()
    if 'search' in request.GET:
        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            cd = searchform.cleaned_data
            ss = core_search(cd['search'])
            results = ss.execute()
            # count total results
        return render(request, 'doctors/post/test.html',
                      {'searchform': searchform,
                       'cd': cd,
                       'results': results })

    return render(request, 'index.html', {'searchform': searchform, })



def cat(request) :

    loc_root_list = []
    loc_root_object = []

    spec_root_list = []
    spec_root_object = []

    loc_shet =[]
    spec_shet = []

    loc_list = {}
    loc_list = {}
    spec_list = {}

    loc_cat_root = Loc_Category.objects.all()

    for loc in loc_cat_root:
        if loc.is_root_node() == True :
            loc_root_list.append(loc.name)
            loc_root_object.append(loc)

    for root in loc_root_object:
        loc_shet = []
        for child in root.get_children()  :
            loc_shet.append(child.name)
            loc_list[root.name] = loc_shet

    spec_cat_root = Spec_Category.objects.all()

    for spec in spec_cat_root:
        if spec.is_root_node() == True:
            spec_root_list.append(spec.name)
            spec_root_object.append(spec)

    return loc_root_list



def searchForm(request) :
    # -------------------------------------------------------------------
    # Main Search
    # -------------------------------------------------------------------
    searchform = SearchForm()
    if 'search' in request.GET:
        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            cd_search = searchform.cleaned_data
            ss_search = core_search(cd_search['search'])
            searchresults = ss_search.execute()
            # count total results
            return render(request, 'doctors/post/test.html',
                          {'results': [hit for hit in searchresults], 'searchform': searchform})



#ToDo : talk about system analysis with group
#ToDo : remove Additional code

@csrf_exempt
def filter_form(request):

    # -------------------------------------------------------------------
    # Filter Search
    # ------------------------------------------------------------------

    loc_root_list = []
    loc_child_list = []
    loc_root_object = []

    spec_root_list = []
    spec_root_object = []

    loc_list = {}

    loc_cat_root = Loc_Category.objects.all()

    for loc in loc_cat_root:
        if loc.is_root_node() == True:
            loc_root_list.append((loc.name, loc.name))
            loc_root_object.append(loc)

    for loc in loc_cat_root:
        if loc.is_child_node() == True:
            loc_child_list.append((loc.name, loc.name))

    for root in loc_root_object:
        loc_shet = []
        for child in root.get_children():
            loc_shet.append((child.name, child.name))
            loc_list[root.name] = loc_shet

    spec_cat_root = Spec_Category.objects.all()

    for spec in spec_cat_root:
        if spec.is_root_node() == True:
            spec_root_list.append(spec.name)
            spec_root_object.append(spec)

    form = FilterSearchForm(brand_choices=tuple(loc_root_list), car_choices=tuple(loc_child_list), specialty=True)
    if 'car' in request.GET or 'brand' in request.GET or 'specialty' in request.GET:
        form = FilterSearchForm(request.GET, brand_choices=tuple(loc_root_list), car_choices=tuple(loc_child_list),
                                specialty=True)
        form.fields['brand'].required = False
        form.fields['car'].required = False
        form.fields['specialty'].required = False

        if form.is_valid():
            cd = form.cleaned_data
            query_brand = cd['brand']
            query_car = cd['car']
            query_specialty = cd['specialty']

            car_choices = []
            cars = Loc_Category.objects.filter(name=query_brand)
            for car in cars:
                for child in car.get_children():
                    car_choices.append((child.name, child.name))

            ss = core_filter_search(query_brand, query_car, query_specialty)
            results = ss.execute()

            form = FilterSearchForm(brand_choices=tuple(loc_root_list), car_choices=tuple(loc_child_list),
                                    specialty=True)
            searchform = SearchForm()
            searchform.fields['search'].required = False

            # count total results

            return render(request, 'doctors/post/test.html',
                          {'filterform': form,
                           'cd': cd,
                           'results': results, 'spec': query_specialty ,'loc_roots' : loc_root_list , 'loc_list' : loc_list , 'loc_list_select': loc_child_list ,'spec_roots':spec_root_object , 'searchform':searchform})
    # -------------------------------------------------------------------
    # Main Search
    # -------------------------------------------------------------------
    searchform = SearchForm()

    if 'search' in request.GET:
        searchform = SearchForm(request.GET)
        searchform.fields['search'].required = False
        if searchform.is_valid():
            cd_search = searchform.cleaned_data
            ss_search = core_search(cd_search['search'])
            searchresults = ss_search.execute()
            searchform = SearchForm()

            # count total results
            return render(request, 'doctors/post/test.html',
                          {'results': [hit for hit in searchresults],'loc_roots' : loc_root_list , 'loc_list' : loc_list , 'loc_list_select': loc_child_list ,'spec_roots':spec_root_object , 'searchform': searchform, 'filterform':form})

    return render(request , 'index.html' , {'loc_roots' : loc_root_list , 'loc_list' : loc_list , 'loc_list_select': loc_child_list ,'spec_roots':spec_root_object , 'filterform': form , 'searchform' : searchform})


# def post_search(request) :
#     form = SearchForm()
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid() :
#             cd = form.cleaned_data
#             results = SearchQuerySet().models(DoctorsPost).filter(content=cd['query']).load_all()
#
#             #count total results
#             total_results = results.count()
#
#         return render(request,'doctors/post/search.html',
#                       {'form' : form,
#                         'cd' : cd,
#                         'results' : results,
#                         'total_results' : total_results})
#
#     return render(request, 'doctors/post/search.html', {'form':form, })

@csrf_exempt
def post_list(request , tag_slug=None , category_slug = None) :

    # search = Search(request)

    object_list = DoctorsPost.objects.all()
    tag = None
    category = None
    child = None
    cat_list = None

    if category_slug:
        category = get_object_or_404(Spec_Category , slug =category_slug)
        object_list = object_list.filter(spec_category__in=[category])

    if tag_slug:
        tag = get_object_or_404(Tag , slug = tag_slug)
        object_list = object_list.filter(tags__in=[tag])


    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'doctors/post/test.html',
                  {'page':page,
                   'posts': posts,
                   'tag':tag ,
                   'category': category ,
                    })





# class PostListView(ListView):
#     queryset = DoctorsPost.objects.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'doctors/post/list.html'

# class EditPost(DetailView):
#     model = DoctorsPost
#     form_class = MapForm
#     template_name = 'doctors/post/detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

@csrf_exempt
def post_detail(request, Spec_Category=None, Loc_Category=None , post=None ):

    # -------------------------------------------------------------------
    # Detail Search
    # -------------------------------------------------------------------
    searchform_Detail = searchDetail()
    if 'search' in request.GET:
        searchform_Detail = searchDetail(request.GET)
        if searchform_Detail.is_valid():
            cd_search = searchform_Detail.cleaned_data
            ss_search = core_search(cd_search['search'])
            searchresults = ss_search.execute()
            # count total results
            return render(request, 'doctors/post/test.html', {'results': [hit for hit in searchresults]})



    post = get_object_or_404(DoctorsPost, slug=post,
                             status='published',
                             spec_category__name = Spec_Category ,
                             loc_category__name = Loc_Category)

    category_slug = Loc_Category
    # List of active comments for this post
    comments = post.comments.filter(active = True)
    if request.method == 'POST' :
        # A comment was posted
        comment_form =CommentsForm(data= request.POST)

        if comment_form.is_valid() :
            #create Comment object but don't save to database
            new_comment = comment_form.save(commit=False)
            #Assign the current post to the comment
            new_comment.post = post
            #save the comment to the database
            new_comment.save()
            # return render(request, 'doctors/post/test.html', {'post': post , 'comment_form':comment_form})
    else :
        comment_form = CommentsForm()



    #List of Similar Posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = DoctorsPost.objects.filter(tags__in=post_tags_ids).exclude(id = post.id)
    #show most recent post with Count('tags')
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags' , '-publish')[:4]
    share_string = quote_plus(post.content)
    Mapform = MapForm()

    is_liked = False
    if post.likes.filter(id = request.user.id).exists():
        is_liked = True

    hit = record_view(request , post)

    context = {}

    context['meta'] = post.as_meta()
    context['post'] = post
    context['comments'] = comments
    context['comment_form'] = comment_form
    context['similar_posts'] = similar_posts
    context['is_liked'] = is_liked
    context['total_likes'] = post.total_likes()
    context['share_string'] = share_string
    context['hit_count'] = hit
    context['searchDetail'] = searchform_Detail
    context['mapform'] = Mapform

    return render(request,'doctors/post/detail.html',context)


# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip
#
# # ToDo : is request.session in django remove after some time like 15 days ?
# def hit_count(request):
#     if not request.session.session_key:
#         request.session.save()
#     s_key = request.session.session_key
#     ip = get_client_ip(request)
#     url, url_created = UrlHit.objects.get_or_create(url=request.path)
#
#     if url_created:
#         track, created = HitCount.objects.get_or_create(url_hit=url, ip=ip, session=s_key)
#         if created:
#             url.increase()
#             request.session[ip] = ip
#             request.session[request.path] = request.path
#     else:
#         if ip and request.path not in request.session:
#             track, created = HitCount.objects.get_or_create(url_hit=url, ip=ip, session=s_key)
#             if created:
#                 url.increase()
#                 request.session[ip] = ip
#                 request.session[request.path] = request.path
#     return url.hits
#     # return "helllo"

def record_view(request, post):

    if not QuestionView.objects.filter(
                    question=post,
                    session=request.session.session_key):
        view = QuestionView(question=post,
                            ip=request.META['REMOTE_ADDR'],
                            created=datetime.datetime.now(),
                            session=request.session.session_key)
        view.save()

    return QuestionView.objects.filter(question=post).count()

# def opening_hours(request):
#     template_name = 'admin/Doctors/OpeningHours/change_list.html'
#     heading_message = 'Formset Demo'
#
#     WEEKDAYS = ["جمعه", "پنج شنبه", "چهارشنبه", "سه شنبه", "دو شنبه", "یک شنبه", "شنبه"]
#     someformset = openingHoursFormSet(initial=[{'weekday': day} for day in WEEKDAYS])
#
#     if request.method == 'GET':
#         formset = openingHoursFormSet(request.GET or None)
#     elif request.method == 'POST':
#         formset = openingHoursFormSet(request.POST)
#         if formset.is_valid():
#             for form in formset:
#                 # extract name from each form and save
#                 from_hour = form.cleaned_data.get('from_hour')
#                 to_hour = form.cleaned_data.get('to_hour')
#                 # save book instance
#
#                 if someformset:
#                     OpeningHours(weekday=someformset).save()
#                 if from_hour:
#                     OpeningHours(from_hour =from_hour).save()
#                 if to_hour:
#                     OpeningHours(to_hour =to_hour).save()
#
#
#             # once all books are saved, redirect to book list view
#             return redirect('book_list')
#     return render(request, template_name, {
#         'formset': formset,
#         'heading': heading_message
#     })

def like_post(request):
    post = get_object_or_404(DoctorsPost, id = request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())


# def show_category(request, hierarchy=None):
#     category_slug = hierarchy.split('/')
#     parent = None
#     root = Spec_Category.objects.all()
#
#     for slug in category_slug[:-1]:
#         parent = root.get(parent=parent, slug=slug)
#
#     try:
#         instance = Spec_Category.objects.get(parent=parent, slug=category_slug[-1])
#         children = instance.children.all()
#         post_set = instance.post_set.all()
#         if not request.user.is_staff or not request.user.is_superuser:
#             post_set = instance.post_set.active()
#         context = {
#             'slug_list': instance.get_slug_list_for_categories(),
#             'children': children,
#             'post_set': post_set
#         }
#     except:
#         posts = DoctorsPost.objects.all()
#         if not request.user.is_staff or not request.user.is_superuser:
#             posts = DoctorsPost.objects.active()
#         instance = get_object_or_404(posts, slug=category_slug[-1])
#         return redirect(reverse('doctors:post_detail', kwargs={'slug': instance.slug}))
#     else:
#         return render(request, 'doctors/categories.html', context)

# TODO : is this optimized ?

def cat_list(request) :

    loc_root_list = []
    loc_root_object = []

    spec_root_list = []
    spec_root_object = []

    loc_shet =[]
    spec_shet = []

    loc_list = {}
    loc_list = {}
    spec_list = {}

    loc_cat_root = Loc_Category.objects.all()

    for loc in loc_cat_root:
        if loc.is_root_node() == True :
            loc_root_list.append(loc.name)
            loc_root_object.append(loc)

    for root in loc_root_object:
        loc_shet = []
        for child in root.get_children()  :
            loc_shet.append(child.name)
            loc_list[root.name] = loc_shet

    spec_cat_root = Spec_Category.objects.all()

    for spec in spec_cat_root:
        if spec.is_root_node() == True:
            spec_root_list.append(spec.name)
            spec_root_object.append(spec)


    return render(request, 'index.html',
                  {'loc_roots' : loc_root_list , 'loc_list' : loc_list , 'spec_roots':spec_root_object  })



# def openinghours(request):
#     general_set = openingHoursFormSet(request.POST)
#     if general_set.is_valid():
#         for form in general_set.forms:
#
#     return render("template.html", {'form': general_set}, RequestContext(request))

# class PostCategory(ListView) :
#     model = DoctorsPost
#     template_name = 'doctors/post/post_category.html'
#
#     def get_queryset(self):
#         self.category = get_object_or_404(Category , pk=self.kwargs['pk'])
#         self.post_by_category = DoctorsPost.objects.filter(category=self.category)
#
#
#     def get_context_data(self , **kwargs):
#         context = super(PostCategory, self).get_context_data(**kwargs)
#         context.update({'category' : self.category ,
#                         'posts' : self.post_by_category })
#         return context
#