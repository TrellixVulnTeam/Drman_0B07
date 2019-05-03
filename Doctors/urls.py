from django.conf.urls import url, include
# from gallery.settings import ROOT_URL
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views

# from django.conf.urls.defaults import *
# from gallery.items.models import Item, Photo

# TODO : check that this url is really good for seo ?

app_name = 'Doctors'

urlpatterns = [
                  # post views
                  url(r'^list/$', views.post_list, name='post_list'),
                  url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
                  url(r'^cat/(?P<category_slug>[^/]+)/$', views.post_list, name='post_list_by_cat'),
                  url(r'^(?P<Spec_Category>[^/]+)/(?P<Loc_Category>[^/]+)/(?P<post>[^/]+)/?$', views.post_detail,
                      name='post_detail'),

                  url(r'^(?P<Spec_Category>[^/]+)/(?P<Loc_Category>[^/]+)/(?P<post>[^/]+)/?', views.completion_suggester, name='completion_suggester'),
                  url(r'^dropdown/', views.cat_list, name="dropdown"),
                  # url(r'^$', views.multiple_forms, name='multi_search'),
                  # url(r'^', views.completion_suggester, name='completion_suggester'),

                  # url(r'^doctors/', views.DoctorsViewSet,name='doctors'),

                  # url(r'^%s' % ROOT_URL[1:], include('gallery.real_urls')),
                  # url(r'^$', 'simple.direct_to_template',kwargs={'template': 'index.html', 'extra_context':
                  #         {'item_list': lambda: Item.objects.all()}},name='index'),
                  # url(r'^items/$', 'list_detail.object_list',kwargs={'queryset': Item.objects.all(),
                  #                                                    'template_name': 'items_list.html','allow_empty': True},name='item_list'),
                  # url(r'^items/(?P<object_id>\d+)/$', 'list_detail.object_detail',kwargs={'queryset': Item.objects.all(),
                  #                                                                         'template_name': 'items_detail.html'},name='item_detail'),
                  # url(r'^photos/(?P<object_id>\d+)/$', 'list_detail.object_detail',kwargs={'queryset': Photo.objects.all(),'template_name': 'photos_detail.html'},name='photo_detail'),
                  # url(r'^cat/(?P<category_slug>[-\w]+)/$', views.post_detail, name='category'),
                  # url(r'^(?P<tag_slug>[-\w]+)/(?P<hierarchy>.+)/$', views.post_list, name='post_list_by_tag'),
                  # url(r'^$', views.PostListView.as_view(), name='post_list'),,

                  # url(r'^category/(?P<hierarchy>.+)/$', views.show_category,name='category'),
                  url(r'^like/$', views.like_post, name='like_post'),
                  # url(r'^opening_hours/$',views.opening_hours, name='opening_hours' ),
                  # url(r'^category/(?P<hierarchy>.+)/$', views.post_detail,name='post_detail_cat'),
                  # url(r'^post/cat/(?P<pk>[-\w]+)/$', views.PostCategory.as_view(), name='post_by_category'),
                  # url(r'^category/$', views.all_category, name='all_category'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# TODO:
# 1.https://karajtabliq.ir/%D8%A7%D8%B7%D9%84%D8%A7%D8%B9%D8%A7%D8%AA-%DA%A9%D8%B1%D8%AC/71
# 2. use like this : کرج/قلب و عروق
# 3. https://nobat.ir/118/?q=%D9%81%D9%88%D9%82+%D8%AA%D8%AE%D8%B5%D8%B5+%DA%A9%D9%88%D8%AF%DA%A9%D8%A7%D9%86+%D9%88+%D8%A7%D8%B7%D9%81%D8%A7%D9%84+%D8%AF%D8%B1+%DA%A9%D8%B1%D8%AC
# 4.
