from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import GenericGroupNode

class Query(BaseQuery):
    genericGroups = DjangoFilterConnectionField(
        GenericGroupNode,
        description = "A list of generic group",
        resolver = resolve.all_generic_group
    )
