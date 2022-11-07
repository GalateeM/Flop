from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import TutorType

class Query(BaseQuery):
    tutors = DjangoFilterConnectionField(
        TutorType,
        description = "A list of tutors",
        resolver = resolve.all_tutors
    )

