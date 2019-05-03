# from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
#
# from . import elastic_search_connection
#
#
# class DoctorDocumentSerializer(DocumentSerializer):
#     class Meta:
#         document = elastic_search_connection.DoctorsIndex
#         fields = (
#             'title',
#             'content',
#             'publish'
#         )