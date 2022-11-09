from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from base.models import RoomType

class RoomTypeNode(DjangoObjectType):
    class Meta:
        model = RoomType
        filter_fields = {
            'department__name' : ['icontains', 'istartswith'],
            'department__abbrev' : ['exact'],
            'name' : ['istartswith', 'icontains']
        }
        fields = ("id", "name")
        interfaces = (relay.Node, )