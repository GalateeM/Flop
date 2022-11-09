from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from quote.models import Quote

class QuoteNode(DjangoObjectType):
    model = Quote
    filter_fields = {
        'quote' : ['icontains', 'istartswith'],
        'last_name' : ['icontains', 'istartswith'],
        'for_name' : ['icontains', 'istartswith'],
        'nick_name' : ['icontains', 'istartswith'],
        'desc_author' : ['icontains', 'istartswith'],
        'date' : ['icontains', 'istartswith'],
        'header' : ['icontains', 'istartswith'],
        'quote_type__name' :['icontains', 'istartswith'],
        'quote_type__abbrev' :['icontains', 'istartswith'],
        'positive_votes' : ['exact'],
        'negative_votes' : ['exact'],
        'id_acc' : ['exact'],
        'statut' : ['icontains', 'istartswith']
    }
    fields = '__all__'
    interfaces = (relay.Node, )