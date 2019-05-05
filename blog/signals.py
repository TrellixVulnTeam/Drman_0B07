from blog.models import Post
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Post)
def index_blogs(sender, instance, **kwargs):
    instance.indexing()
