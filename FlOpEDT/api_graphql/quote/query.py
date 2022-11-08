from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import QuoteNode

class Query(BaseQuery):
    quotes = DjangoFilterConnectionField(
        QuoteNode,
        description = "A list of quote",
        resolver = resolve.all_quote
    )