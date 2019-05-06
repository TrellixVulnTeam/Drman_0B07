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
class BlogIndex(DocType):

    text = Text()
    title = Text()
    title_suggest = Completion()

    cat = fields.StringField(
        attr='cat_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword', multi=True),
            'suggest': fields.CompletionField(),
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

    publish = Date(format="yyyy-MM-dd")
    author = Text()


    class Meta:
        index = 'blog'

def manual_index():
    BlogIndex.init()

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

    bulk(client=es, actions=(b.indexing() for b in models.Post.objects.all().iterator()))
