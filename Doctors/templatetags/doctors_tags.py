from django import template
from django.db.models import Count
# from blog.models import Post
from django.utils.safestring import mark_safe
import markdown
# from ..models import Category

register = template.Library()

from ..models import DoctorsPost

@register.simple_tag
def total_posts() :
    return DoctorsPost.objects.count()



# @register.inclusion_tag('doctors/post/latest_posts.html')
# def show_latest_posts(count) :
#     latest_posts = Post.objects.order_by('-publish')[:count]
#     return {'latest_posts':latest_posts}

@register.simple_tag
def get_most_viewed_posts(count=8) :
    return DoctorsPost.objects.annotate(total_comments = Count('questionviews')).order_by('-total_comments')[:count]

@register.filter
def get_name(value):
    spam = value.split('/')[-1]         # assume value be /python/web-scrapping
                                        # spam would be 'web-scrapping'
    spam = ' '.join(spam.split('-'))    # now spam would be 'web scrapping'
    return spam

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))




# @register.simple_tag
# def get_cat():
#     roots = Category.objects.root_nodes()
#
#     return roots
