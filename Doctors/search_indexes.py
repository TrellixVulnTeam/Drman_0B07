# from haystack import indexes
# from .models import DoctorsPost
#
# class PostIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True, template_name="search/doctors_text.txt")
#     title = indexes.CharField(model_attr='title')
#     publish = indexes.DateTimeField(model_attr='publish')
#
#
#     def get_model(self):
#         return DoctorsPost
#
#     def index_queryset(self, using=None):
#         return self.get_model().objects.all()
