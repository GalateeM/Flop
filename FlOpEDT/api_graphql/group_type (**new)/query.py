from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import GroupTypeNode

class Query(BaseQuery):
    groupTypes = DjangoFilterConnectionField(
        GroupTypeNode,
        description = "A list of group types",
        resolver = resolve.all_group_type
    )
