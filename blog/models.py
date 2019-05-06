from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils.translation import ugettext_lazy as _
from mptt.models import TreeManyToManyField
from Doctors.models import Category
from django.template.defaultfilters import slugify
from .search import BlogIndex
from elasticsearch import Elasticsearch
from filer.fields.image import FilerImageField
from meta.models import ModelMeta
import json

class Categories(Category):

    class Meta:
        unique_together = (('parent', 'slug', ))
        verbose_name = _("دسته بندی")
        verbose_name_plural = _("دسته بندی ها")


    def __str__(self):
        return self.name

class Post(ModelMeta,models.Model) :
    STATUS_CHOISES = (
        ('draft' , 'Draft') ,
        ('published' , 'Published') ,
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(allow_unicode=True)

#TODO : study about on_delete from doc
    
    author = models.ForeignKey(User , related_name='blog_posts' , on_delete=models.CASCADE)
    body = models.TextField()
    thumbnailImage = FilerImageField(on_delete=models.CASCADE, related_name="blog_thumb_image")
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    tags = TaggableManager()
    categories = TreeManyToManyField(Categories , related_name="categories")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10 ,
                              choices=STATUS_CHOISES ,
                              default="draft")


    class Meta:
        ordering = ('-publish' ,)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def blog_views_count(self):
        return self.views.count()

    def cat_indexing(self):
        """«category for indexing.

        Used in Elasticsearch indexing.
        """
        data = json.dumps([cat.name for cat in self.categories.all()],ensure_ascii=False)
        jsondata = json.loads(data)
        return jsondata

    title_suggest = []

    def indexing(self):
        obj = BlogIndex(
            meta={ 'index': 'blog'},
            title=self.title,
            title_suggest =  [
                {

                    "input": [self.title ],
                    "weight": 34
                },
                {
                    "input": self.cat_indexing(),
                },
                {
                    "input": [tag.name for tag in self.tags.all()],
                }
            ],

            text=self.body,
            cat=self.cat_indexing(),
            publish=self.publish,
            author=self.author.username,
            thumbnailImage=self.thumbnailImage.url,
            views=self.blog_views_count(),
            url=self.get_absolute_url()


        )
        es = Elasticsearch(['http://elasticsearch613:9200/'])
        obj.save(es, request_timeout=80)
        return obj.to_dict(include_meta=True)


    def get_absolute_url(self):
        cat = []
        for x in self.categories.all():
            cat = x.name

        return reverse('blog:post_detail', args=[cat , self.slug])

    def save(self, *args, **kwargs):
        if self.slug in (None, '', u''):
            self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs)

    #  Keywords for django seo

    _metadata = {
        'title': 'title',
        'description': 'content',
        'keywords' : 'tag_indexing'
    }



class Comments(models.Model) :
    post = models.ForeignKey(Post , related_name='comments' , on_delete=models.CASCADE,)
    name = models.CharField(max_length=250)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name , self.post)


class View(models.Model):
    question = models.ForeignKey(Post, related_name='views' , on_delete=models.CASCADE , null=True)
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now=True)