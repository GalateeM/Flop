from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from base.models import Room

class RoomNode(DjangoObjectType):
    class Meta:
        model = Room
        filter_fields = {
            'departments__name' : ['icontains', 'istartswith'],
            'departments__abbrev' : ['exact'],
            'types__name' : ['istartswith', 'icontains']
        }
        fields = ("id", "name", "types", "subroom_of", "departments")
        interfaces = (relay.Node, )
