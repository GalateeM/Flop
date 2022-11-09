from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from quote.models import QuoteType

class QuoteTypeNode(DjangoObjectType):

    class Meta:
        model = QuoteType
        filter_fields = {
            'name' : ['exact', 'icontains', 'istartswith'],
            'abbrev' : ['exact'],
            'parent__abbrev' : ['exact'],
            'parent__name' : ['exact', 'icontains', 'istartswith']
        }
        fields = '__all__'
        interfaces = (relay.Node, )
