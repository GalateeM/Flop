rom graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import QuoteType

class Query(BaseQuery):
    quote = DjangoFilterConnectionField(
        QuoteType,
        description = "A list of quote",
        resolver = resolve.
    )