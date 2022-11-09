from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import PeriodType

class Query(BaseQuery):
    periods = DjangoFilterConnectionField(
        PeriodType,
        description = "A list of periods",
        resolver = resolve.all_periods
    )