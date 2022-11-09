from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import WeekType

class Query(BaseQuery):
    weeks = DjangoFilterConnectionField(
        WeekType,
        description = "A list of weeks",
        resolver = resolve.all_weeks
    )