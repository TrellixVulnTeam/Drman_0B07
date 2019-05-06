from django.conf.urls import url
from . feeds import LatestPostsFeed
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView )

app_name = 'blog'


urlpatterns = [
    # post views

    url(r'^$', views.post_list, name='post_list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
    url(r'^cat/(?P<category_slug>[^/]+)/$', views.post_list, name='post_list_by_cat'),
    #url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^(?P<cat>[^/]+)/(?P<post>[^/]+)/?$', views.post_detail,name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$' , views.post_share , name='post_share') ,
    url(r'^feed/$', LatestPostsFeed(), name='post_feed'),
    # url(r'^search/$', views.post_search, name='post_search'),
    # login / logout urls
    # url(r'^login/$',LoginView.as_view() ,name='login'),
    # url(r'^logout/$',LogoutView.as_view() ,name='logout'),
    # url(r'^logout-then-login/$', auth_views.logout_then_login ,name='logout_then_login'),
    url(r'^$', views.dashboard, name='dashboard'),
    # change password urls
url(r'^password-change/$',PasswordChangeView.as_view(),name='password_change'),
    url(r'^password-change-done/$',PasswordChangeDoneView.as_view(), name='password_change_done'),
    # restore password urls
    url(r'^password-reset/$', PasswordResetView.as_view() ,name='password_reset'),
    url(r'^password-reset-done/$', PasswordResetDoneView.as_view() ,name='password_reset_done'),
    url(r'^password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    url(r'^password-reset-complete/$', PasswordResetCompleteView.as_view() ,name='password_reset_complete'),
    url(r'^like/$',views.like_post, name='like_post' ),
]
