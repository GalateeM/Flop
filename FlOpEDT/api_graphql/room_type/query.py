from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import RoomTypeNode


class Query(BaseQuery):
    roomType = DjangoFilterConnectionField(
        RoomTypeNode,
        description="A list of room type",
        resolver=resolve.all_room_type
    )
