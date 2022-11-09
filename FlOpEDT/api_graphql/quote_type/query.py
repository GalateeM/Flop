from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import QuoteTypeNode

class Query(BaseQuery):
    quoteTypes = DjangoFilterConnectionField(
        QuoteTypeNode,
        description = "A list of quote types",
        resolver = resolve.all_quote_types
    )
