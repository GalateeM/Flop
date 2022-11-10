from graphene import List, String, relay
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve
from .filter import RoomFilter

from .types import RoomNode


class Query(BaseQuery):
    rooms = DjangoFilterConnectionField(RoomNode)