from django.conf.urls import include, url
from django.contrib import admin

# media in ckeditor Editor
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from Doctors.sitemaps import DrsPostSitemap

# Sitemap
from django.contrib.sitemaps.views import sitemap
# from blog.sitemaps import PostSitemap
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from Doctors import views

sitemaps = {
    'posts': DrsPostSitemap(),
}



urlpatterns = [
                  # url(r'^$', views.multiple_forms, name='search_form'),
                  url(r'^$', views.filter_form, name='filter_search'),
                  url(r'^i18n/', include('django.conf.urls.i18n')),
                  url(r'^jet/', include(('jet.urls', 'jet'), namespace='jet')),  # Django JET URLS
                  url(r'^jet/dashboard/', include(('jet.dashboard.urls', 'jet-dashboard'), namespace='jet-dashboard')),
                  url(r'^admin/', admin.site.urls),
                  # url(r'^login/$', auth_views.login, name='login'),
                  # url(r'^logout/$', auth_views.logout, name='logout'),
                  url(r'^blog/', include(('blog.urls', 'blog'), namespace='blog')),
                  url(r'^doctors/', include(('Doctors.urls', 'doctors'), namespace='doctors')),
                  url(r'^sitemap.xml$', sitemap, {'sitemaps': sitemaps},
                      name='django.contrib.sitemaps.views.sitemap'),
                  url(r'^ckeditor/', include('ckeditor_uploader.urls')),
                  url(r'^djga/', include('google_analytics.urls')),
                  url(r'^media/(?P<path>.*)$', serve, {
                      'document_root': settings.MEDIA_ROOT
                  }),
                  url(r'^', views.completion_suggester, name='completion_suggester'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# media in ckeditor Editor
# serving media files only on debug mode
# if settings.DEBUG:
#     urlpatterns += [
#         url(r'^media/(?P<path>.*)$', serve, {
#             'document_root': settings.MEDIA_ROOT
#         }),
#     ]
