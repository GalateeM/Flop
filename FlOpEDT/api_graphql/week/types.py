from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from base.models import Week

class WeekType(DjangoObjectType):

    class Meta:
        model = Week
        filter_fields = {
            'nb' : ['exact'],
            'year' : ['exact']
        }
        fields = '__all__'
        interfaces = (relay.Node, )