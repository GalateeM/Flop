from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from base.models import Period

class PeriodType(DjangoObjectType):

    class Meta:
        model = Period
        filter_fields = {
            'department__name' : ['icontains', 'istartswith'],
            'name' : ['exact']
        }
        fields = '__all__'
        interfaces = (relay.Node, )