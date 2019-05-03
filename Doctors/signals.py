from .models import DoctorsPost
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=DoctorsPost)
def index_doctors(sender, instance, **kwargs):
    instance.indexing()