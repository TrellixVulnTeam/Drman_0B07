from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm , CommentsForm , SearchForm
from .models import Post , Comments , Categories
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth.decorators import login_required



from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.http import HttpResponseRedirect

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q

from django.views.decorators.csrf import csrf_exempt

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                    'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})


def core_search(query):
    es = Elasticsearch(['http://elasticsearch613:9200/'])
    q = Q("multi_match", query=query, fields=['title', 'text', 'cat', 'tags' ])

    ss = Search(using=es, index='blog').query(q)
    return ss

# TODO: how we can use search in separate view


# def search_form(request) :
#     searchform = SearchForm()
#
#     if 'search' in request.GET:
#         searchform = SearchForm(request.GET)
#         searchform.fields['search'].required = False
#         if searchform.is_valid():
#             cd_search = searchform.cleaned_data
#             ss_search = core_search(cd_search['search'])
#             searchresults = ss_search.execute()
#             searchform = SearchForm()
#
#             return render(request, 'blog/post/search.html',
#                           {'results': [hit for hit in searchresults], 'searchform': searchform})

def category_list(request):
    cat_list = []
    categories = Categories.objects.all()
    for cat in categories :
        cat_list.append(cat)
    return cat_list

@csrf_exempt
def post_list(request, tag_slug=None, category_slug=None):

    object_list = Post.objects.all()
    tag = None
    category = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    if category_slug:
        category = get_object_or_404(Categories, slug=category_slug)
        object_list = object_list.filter(categories__in=[category])

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

            return render(request, 'blog/post/search.html',
                          {'results': [hit for hit in searchresults], 'searchform': searchform})

    # -------------------------------------------------------------------
    # Categories list
    # -------------------------------------------------------------------
    cat_list = category_list(request)

    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag,
                   'cat_list': cat_list,
                   'category': category,
                   'searchform': searchform})


class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, cat=None, post=None):

    try:
        post = get_object_or_404(Post, slug=post,
                                 status='published',
                                 categories__name = cat )
    except Post.DoesNotExist:
        post = None

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
    else :
        comment_form = CommentsForm()


    #List of Similar Posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id = post.id)
    #show most recent post with Count('tags')
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags' , '-publish')[:4]

    is_liked = False
    if post.likes.filter(id = request.user.id).exists():
        is_liked = True

    # -------------------------------------------------------------------
    # Categories list
    # -------------------------------------------------------------------
    cat_list = category_list(request)

    return render(request, 'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts,
                   'is_liked': is_liked,
                   'total_likes': post.total_likes(),
                   'cat_list': cat_list
                   })


def like_post(request):
    post = get_object_or_404(Post, id = request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())



def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'] , cd['email'] , post.title)
            message = 'Read "{}" at {}\n\n\'s comments: {}'.format(post.title, post_url , cd['name'] , cd['comments'])
            send_mail(subject, message, 'avaa.torabli@gmial.com' , [cd['to']])
            sent = True
            # ... send email
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


@login_required
def dashboard(request):
    return render(request,'blog/dashboard.html',{'section': 'dashboard'})

