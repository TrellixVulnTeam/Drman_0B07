# from django_elasticsearch_dsl import DocType, Index ,fields
# import time
#
#
# connected = False
#
# while not connected:
#     try:
#         es.info()
#         connected = True
#     except ConnectionError:
#         print("Elasticsearch not available yet, trying again in 2s...)
#         time.sleep(2)
# # from elasticsearch_dsl import analyzer
# from . import models
#
# doctors = Index('doctorss')
#
# # reference elasticsearch doc for default settings here
# # doctors.settings(
# #     number_of_shards=1,
# #     number_of_replicas=0
# # )
# #
# # html_strip = analyzer(
# #     'html_strip',
# #     tokenizer="standard",
# #     filter=["standard", "lowercase", "stop", "snowball"],
# #     char_filter=["html_strip"]
# # )
#
# @doctors.doc_type
# class DoctorsIndex(DocType):
#
#     # title = fields.StringField(
#     #     analyzer=html_strip,
#     #     fields={
#     #         'raw': fields.StringField(analyzer='keyword'),
#     #     }
#     # )
#     # content = fields.TextField(
#     #     analyzer=html_strip,
#     #     fields={
#     #         'raw': fields.TextField(analyzer='keyword'),
#     #     }
#     # )
#     # publish = fields.DateField()
#
#     class Meta:
#         model = models.DoctorsPost
#
#
#         fields = [
#             'title' ,
#             # 'content' ,
#             # 'publish' ,
#         ]