from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from base.models import GroupType

class GroupTypeNode(DjangoObjectType):

    class Meta:
        model = GroupType
        filter_fields = {
            'name' : ['icontains', 'istartswith'],
            'department__name' : ['icontains', 'istartswith'],
            'department__abbrev' : ['exact']
        }
        fields = '__all__'
        interfaces = (relay.Node, )
