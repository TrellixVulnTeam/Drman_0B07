from django.contrib.sitemaps import Sitemap
from Doctors.models import DoctorsPost
from Drman.settings import LANGUAGE_CODE

class DrsPostSitemap(Sitemap) :
    changegreq = 'daily'
    priority = 0.9

    def items(self):
        return DoctorsPost.objects.all()

    def lastmod(self, obj):
        return obj.publish