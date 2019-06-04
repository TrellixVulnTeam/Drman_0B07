from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField,TreeOneToOneField
from django.utils.translation import ugettext_lazy as _
# from .forms import openingHoursForm
from django.contrib import admin



# editor
from ckeditor_uploader.fields import RichTextUploadingField
from filer.fields.image import FilerImageField

from django.template.defaultfilters import slugify

from django.forms import BaseInlineFormSet
from django import forms

from .search import DoctorsIndex
from elasticsearch import Elasticsearch
from djgeojson.fields import PointField
from leaflet.admin import LeafletGeoAdmin

from django.forms.widgets import CheckboxSelectMultiple
from elasticsearch_dsl import Completion
import json
from meta.models import ModelMeta
# from .search import manual_index

from django.forms import formset_factory

from .fields import SeparatedValuesField




#
# class Styles(models.Model):
#     name = models.CharField(max_length=20)
#     info = JSONField(default={})
#
# class Categories(models.Model):
#     name = models.CharField(max_length=20)
#     styles = models.ForeignKey(Styles)

DAYS_OF_WEEK = (
    (0, 'شنبه'),
    (1, 'یک شنبه'),
    (2, 'دو شنبه'),
    (3, 'سه شنبه'),
    (4, 'چهار شنبه'),
    (5, 'پنج شنبه'),
    (6, 'جمعه'),
)


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, db_index=True, on_delete=models.CASCADE, related_name="category")
    # TODO : make auto slug from the name
    slug = models.SlugField(allow_unicode=True)


    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.slug in (None, '', u''):
            self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)


    def __str__(self):
        return self.name

class Loc_Category(Category):

    class Meta:
        unique_together = (('parent', 'slug', ))
        verbose_name = _("موقعیت")
        verbose_name_plural = _("لیست موقعیت ها")

    def get_slug_list(self):
        for x in Loc_Category.all():
            loc_cat = x.slug
        return loc_cat

    def __str__(self):
        return self.name


class Spec_Category(Category):

    class Meta:
        unique_together = (('parent', 'slug', ))
        verbose_name = _("تخصص")
        verbose_name_plural = _("لیست تخصص ها")


    def __str__(self):
        return self.name



class Map(models.Model):

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    description = models.TextField()
    geom = PointField()

    def __unicode__(self):
        return self.title

# # see book Python Web Development with Django with permission
# class Item(models.Model):
#
#
#     name = models.CharField(max_length=250)
#     description = models.TextField()
#     class Meta:
#         ordering = ['name']
#     def __unicode__(self):
#         return self.name
#
#     # @permalink
#     def get_absolute_url(self):
#         return ('item_detail.html', None, {'object_id': self.id})


#
# class ItemAdmin(admin.ModelAdmin):
#     inlines = [PhotoInline]


class DoctorsPost(ModelMeta,models.Model):
    STATUS_CHOISES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    # TODO : rename to Doctor's name
    title = models.CharField(max_length=250 , unique = True)
    thumbnailImage = FilerImageField(on_delete=models.CASCADE , related_name="thumbnailImage")
    mainPhoto = FilerImageField(on_delete=models.CASCADE , related_name="mainPhoto")
    slug = models.SlugField(allow_unicode=True)
    # OfficeAddress = models.CharField()

    # TODO : study about on_delete from doc

    author = models.ForeignKey(User, related_name='Doctors_posts', on_delete=models.CASCADE)
    content = RichTextUploadingField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    loc_category = TreeManyToManyField(Loc_Category,verbose_name=_("Loc_Category") , related_name="loc_category")
    spec_category = TreeManyToManyField(Spec_Category,verbose_name=_("Spec_Category") , related_name="spec_category")
    # map = models.ForeignKey(Map, related_name='map', on_delete=models.CASCADE, null=True)
    likes = models.ManyToManyField(User, related_name='doctors_likes', blank=True)
    # PhotoGallery = models.ForeignKey(Photo, related_name='PhotoGallery', on_delete=models.CASCADE, null=True)
    tags = TaggableManager(verbose_name=_("تگ ها"))
    # map = models.ForeignKey(Map, related_name='map', on_delete=models.CASCADE)

    # contact = models.CharField(max_length=20)

    site = models.URLField(blank=True)
    address = models.CharField(max_length=250)
    geom = PointField()
    # ActiveOpeningHours = models.BooleanField(default=False)



    status = models.CharField(max_length=10,
                              choices=STATUS_CHOISES,
                              default="draft")



    class Meta:
        ordering = ('-publish',)
        verbose_name = _("پزشک")
        verbose_name_plural = _("لیست پزشک ها")




    def loccat_indexing(self):
        """«Location category for indexing.

        Used in Elasticsearch indexing.
        """
        data = json.dumps([cat.name for cat in self.loc_category.all()],ensure_ascii=False)
        jsondata = json.loads(data)
        return jsondata

    def speccat_indexing(self):
        """«Location category for indexing.

        Used in Elasticsearch indexing.
        """
        data = json.dumps([cat.name for cat in self.spec_category.all()],ensure_ascii=False)
        jsondata = json.loads(data)
        return jsondata

    def tag_indexing(self):
        """«Location category for indexing.

        Used in Elasticsearch indexing.
        """
        data = [tag.name for tag in self.tags.all()]
        return data


    def Doctor_views_count(self):
        return self.questionviews.count()

    title_suggest = []

    # #TODO: is there any way that show thumbnailImage but don't index in elasticsearch.
    def indexing(self):
        obj = DoctorsIndex(
            meta={'id': self.id , 'index' : 'doctor'},
            id = self.id ,
            title=self.title,
            title_suggest =  [
                {

                    "input": [self.title ],
                    "weight" : 34
                } ,
                {
                    "input": self.speccat_indexing(),
                } ,
                {
                    "input": [tag.name for tag in self.tags.all()],
                }
            ] ,

            text = self.content ,
            loc_cat = self.loccat_indexing() ,
            spec_cat = self.speccat_indexing(),
            publish =self.publish ,
            thumbnailImage = self.thumbnailImage.url ,
            views = self.Doctor_views_count() ,
            url = self.get_absolute_url()


        )
        es = Elasticsearch(['http://elasticsearch613:9200/'])
        obj.save(es ,request_timeout=80)
        return obj.to_dict(include_meta=True)


    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        spec_cat = []
        loc_cat = []
        for x in self.spec_category.all():
            spec_cat = x.name
        for y in self.loc_category.all():
            loc_cat = y.name

        return reverse('doctors:post_detail', args=[spec_cat , loc_cat , self.slug])

    def save(self, *args, **kwargs):
        if self.slug in (None, '', u''):
            self.slug = slugify(self.title)

        super(DoctorsPost, self).save(*args, **kwargs)

    #  Keywords for django seo

    _metadata = {
        'title': 'title',
        'description': 'content',
        'keywords' : 'tag_indexing'
    }

class contact(models.Model) :
    doctors = models.ForeignKey(DoctorsPost ,related_name='contact', on_delete=models.CASCADE)
    contact = models.CharField(max_length=20)

class socialMedia(models.Model) :

    doctors = models.ForeignKey(DoctorsPost, related_name='SocialMedia', on_delete=models.CASCADE)
    Twitter = models.URLField(blank=True)
    Instagram = models.URLField(blank=True)
    Telegram = models.URLField(blank=True)
    Whatsapp = models.URLField(blank=True)
    Linkedin = models.URLField(blank=True)

class SocialMediaInlineAdminForm(forms.ModelForm):
    class Meta:
        model = contact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super( SocialMediaInlineAdminForm, self).__init__(*args, **kwargs)

class SocialMediaInline(admin.TabularInline) :
    form =  SocialMediaInlineAdminForm
    model = socialMedia
    extra = 1

class ContactInlineAdminForm(forms.ModelForm):
    class Meta:
        model = contact
        fields = ['contact',]

    def __init__(self, *args, **kwargs):
        super( ContactInlineAdminForm, self).__init__(*args, **kwargs)


class Photo(models.Model):

    item = models.ForeignKey(DoctorsPost,on_delete=models.CASCADE , related_name="Photo")
    title = models.CharField(max_length=100)
    image = FilerImageField(on_delete=models.CASCADE)
    caption = models.CharField(max_length=250, blank=True)
    class Meta:
        ordering = ['title']
    def __unicode__(self):
        return self.title

    # @permalink
    def get_absolute_url(self):
        return ('photo_detail', None, {'object_id': self.id})

#
class PhotoInline(admin.StackedInline):
    model = Photo


# hours = [{
#         'weekday': day,
#
#     } for day in range(0,7)]
#
# class openingFormSet(BaseInlineFormSet):
#
#     def __init__(self, *args, **kwargs):
#         super(openingFormSet, self).__init__(*args, **kwargs)
#         self.initial = hours


# formset = openingFormSet(initial=hours)

class contactHoursInline(admin.TabularInline) :
    form =  ContactInlineAdminForm
    model = contact
    extra = 1



class OpeningHours(models.Model):
    """
    Store opening times of company premises,
    defined on a daily basis (per day) using one or more
    start and end times of opening slots.
    """
    class Meta:
        verbose_name = _('ساعت کاری')  # plurale tantum
        verbose_name_plural = _('ساعات کاری')

    doctors = models.ForeignKey(DoctorsPost,related_name="OpeningHours" , verbose_name=_('DoctorsPost'), on_delete=models.CASCADE)
    is_active = models.BooleanField()
    weekday = models.IntegerField(choices=DAYS_OF_WEEK)
    from_hour = models.TimeField(_('Start'))
    to_hour = models.TimeField(_('End'))
    is_closed = models.BooleanField()

    def __str__(self):
        return _(" %(weekday)s (%(from_hour)s - %(to_hour)s)") % {
            'doctors': self.doctors,
            'weekday': self.weekday,
            'from_hour': self.from_hour,
            'to_hour': self.to_hour
        }

# class day(models.Model) :



# class weekdays(day) :
#     name = models.CharField(max_length=50)

class ClosingRules(models.Model):
    """
    Used to overrule the OpeningHours. This will "close" the store due to
    public holiday, annual closing or private party, etc.
    """
    class Meta:
        verbose_name = _('تاریخ تعطیلی')
        verbose_name_plural = _('تاریخ های تعطیلی')
        ordering = ['start']

    doctors = models.ForeignKey(DoctorsPost, verbose_name=_('DoctorsPost'), on_delete=models.CASCADE)
    start = models.DateTimeField(_('Start'))
    end = models.DateTimeField(_('End'))
    reason = models.TextField(_('Reason'), null=True, blank=True)

    def __str__(self):
        return _("%(doctors)s is closed from %(start)s to %(end)s\
        due to %(reason)s") % {
            'doctors': self.doctors,
            'start': str(self.start),
            'end': str(self.end),
            'reason': self.reason
        }

# class OpeningHoursAdmin(admin.ModelAdmin) :
#
#     change_form_template = 'admin/Doctors/OpeningHours/change_list.html'
    # def openinghourTable(self , obj):
    #     return obj.openinghourTable()
    #
    # readonly_fields = ['openinghourTable']

# class subcategory(models.Model):
#     title = models.CharField(max_length=50, unique=True)
#     parent = TreeOneToOneField('Category', on_delete=models.CASCADE, related_name='subcat')
#     slug = models.SlugField()
#
#     class Meta:
#         verbose_name = _("subCategory")
#         verbose_name_plural = _("SubCategories")
#
#     def __unicode__(self):
#         return self.title





class Comments(models.Model) :
    post = models.ForeignKey(DoctorsPost , related_name='comments' , on_delete=models.CASCADE )
    name = models.CharField(max_length=250)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
        verbose_name = _("نظر")
        verbose_name_plural = _("نظرات")

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name , self.post)



class OpeninghoursInlineAdminForm(forms.ModelForm):
    class Meta:
        model = OpeningHours
        fields = ['weekday','from_hour', 'to_hour' , 'is_closed']

    def __init__(self, *args, **kwargs):
        super( OpeninghoursInlineAdminForm, self).__init__(*args, **kwargs)

hours = [{
        'weekday': day,

    } for day in range(0,7)]

class openingFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(openingFormSet, self).__init__(*args, **kwargs)
        self.initial = hours


# formset = openingFormSet(initial=hours)

class openingHoursInline(admin.TabularInline) :
    form =  OpeninghoursInlineAdminForm
    model = OpeningHours
    extra = 7
    formset = openingFormSet


# class openingHourAdmin(admin.InlineModelAdmin) :
#
#     inlines = [openingHoursInline]


class JetCheckboxSelectMultiple(CheckboxSelectMultiple):
    option_template_name = 'admin/forms/widgets/checkbox_option.html'


# class LocCatForm(forms.ModelForm):
#     user = forms.ModelChoiceField(queryset=Loc_Category.objects.all(), widget=JetCheckboxSelectMultiple)
#     fields = '__all__'
#
#     class Meta:
#         model = Loc_Category
#         fields = '__all__'



class DoctorPostAdmin(LeafletGeoAdmin):
    change_form_template = 'admin/Doctors/DoctorsPost/change_form.html'
    add_form_template = 'admin/Doctors/DoctorsPost/add_form.html'

    # form = LocCatForm

    # class Media:
    #         css = {
    #           'all': ('admin/assets/dist/css/stylehealth.min.css', ) ,
    #         }

    inlines = [openingHoursInline,contactHoursInline,SocialMediaInline,PhotoInline]

    def Doctor_comment_count(self , obj):
        return obj.comments.count()

    # formfield_overrides = {
    #     TreeManyToManyField: {'widget': JetCheckboxSelectMultiple },
    #
    # }

    list_display = ('title'  , 'get_spec_category' , 'get_loc_category' ,'Doctor_comment_count' )

    search_fields = ['title' , 'slug' ]

    prepopulated_fields = {"slug": ("title",)}

    def get_spec_category(self , obj):
        return "\n ,".join([c.name for c in obj.spec_category.all()])

    def get_loc_category(self , obj):
        return "\n ,".join([c.name for c in obj.loc_category.all()])

    Doctor_comment_count.short_description = "تعداد نظر ها"
    get_spec_category.short_description = "دسته بندی تخصص ها"
    get_loc_category.short_description = "دسته بندی موقعیت ها"


class Loc_CategoryAdmin(admin.ModelAdmin) :
    search_fields = ['name' , 'slug']
    prepopulated_fields = {"slug": ("name",)}

class Spec_CategoryAdmin(admin.ModelAdmin) :
    search_fields = ['name' , 'slug']
    prepopulated_fields = {"slug": ("name",)}


# class UrlHit(models.Model):
#     url     = models.URLField()
#     hits    = models.PositiveIntegerField(default=0)
#
#     def __str__(self):
#         return str(self.url)
#
#     def increase(self):
#         self.hits += 1
#         self.save()
#
#
# class HitCount(models.Model):
#     url_hit = models.ForeignKey(UrlHit, editable=False, on_delete=models.CASCADE)
#     ip      = models.CharField(max_length=40)
#     session = models.CharField(max_length=40)
#     date    = models.DateTimeField(auto_now=True)

class QuestionView(models.Model):
    question = models.ForeignKey(DoctorsPost, related_name='questionviews' , on_delete=models.CASCADE , null=True)
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now=True)




# def _add_thumb(s):
#
#     parts = s.split(".")
#     parts.insert(-1, "thumb")
#     if parts[-1].lower() not in ['jpeg', 'jpg']:
#         parts[-1] = 'jpg'
#         return ".".join(parts)
#
# class ThumbnailImageFieldFile(models.ImageFieldFile):
#     def _get_thumb_path(self):
#         return _add_thumb(self.path)
#     thumb_path = property(_get_thumb_path)
#     def _get_thumb_url(self):
#         return _add_thumb(self.url)
#     thumb_url = property(_get_thumb_url)
#
#     def save(self, name, content, save=True):
#         super(ThumbnailImageFieldFile, self).save(name, content, save)
#
#         img = Image.open(self.path)
#         img.thumbnail(
#             (self.field.thumb_width, self.field.thumb_height),
#             Image.ANTIALIAS
#         )
#         img.save(self.thumb_path, 'JPEG')



# class Post(models.Model):
#     title = models.CharField(max_length=120)
#     category = TreeForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)
#     content = models.TextField('Content')
#     slug = models.SlugField()
#
#     def __str__(self):
#         return self.title

# class subCategory(models.Model):
#     name = models.CharField(max_length=200, db_index=True)
#
#
# class Category(models.Model):
#     name = models.CharField(max_length=200,db_index=True)
#     slug = models.SlugField(max_length=200,db_index=True,unique=True)
#     df = models.ForeignKey('subCategory', blank=True, null=True, related_name='fdf' , on_delete=models.CASCADE)
#     parent = models.ForeignKey('self', blank=True, null=True, related_name='children' , on_delete=models.CASCADE)
#     # ToDo : image icon for category item
#     class Meta:
#         unique_together = ('slug', 'parent', 'df')  # enforcing that there can not be two
#         verbose_name_plural = "categories"  # categories under a parent with same
#         # slug
#
#     def __str__(self):  # __str__ method elaborated later in
#         full_path = [self.name]  # post.  use __unicode__ in place of
#         # __str__ if you are using python 2
#         k = self.parent
#
#         while k is not None:
#             full_path.append(k.name)
#             k = k.parent
#
#         return ' -> '.join(full_path[::-1])
