from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve
from .filter import RoomFilter

from base.models import Room

class RoomNode(DjangoObjectType):
    class Meta:
        model = Room
        filterset_class = RoomFilter
        interfaces = (relay.Node, )
