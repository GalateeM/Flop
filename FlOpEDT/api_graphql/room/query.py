from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import RoomNode


class Query(BaseQuery):
    rooms = DjangoFilterConnectionField(
        RoomNode,
        description="A list of rooms",
        resolver=resolve.all_rooms
    )
