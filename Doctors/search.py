from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, Completion , Search,analyzer , Completion , tokenizer ,token_filter
from django_elasticsearch_dsl import fields
from elasticsearch.helpers import bulk

from elasticsearch_dsl.connections import connections
from . import models
import time


html_strip = analyzer('html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


# Create a connection to ElasticSearch
connections.create_connection()

# defines what needs to index in elastic search
class DoctorsIndex(DocType):

    text = Text()
    title = Text()
    title_suggest = Completion()

    loc_cat = fields.StringField(
        attr='loccat_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword', multi=True),
            'suggest': fields.CompletionField(),
        },
        multi=True
    )

    spec_cat = fields.StringField(
        attr='speccat_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword', multi=True),
        },
        multi=True
    )

    thumbnailImage = fields.StringField(
        attr='thumbnailImage',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword', multi=True),
        },
        multi=True
    )

    publish = Date()

    class Meta:
        index = 'doctor'

def manual_index():
    DoctorsIndex.init()

    time.sleep(20)

    es = Elasticsearch(['http://elasticsearch613:9200/'])

    connected = False

    while not connected:
        try:
            es.info()
            connected = True
        except ConnectionError:
            print("Elasticsearch not available yet, trying again in 2s...")
            time.sleep(2)

    bulk(client=es, actions=(b.indexing() for b in models.DoctorsPost.objects.all().iterator()))
