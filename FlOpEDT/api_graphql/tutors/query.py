from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import TutorType, TutorUsername

class Query(BaseQuery):
    tutor = DjangoFilterConnectionField(
        TutorType,
        description = "A list of tutors",
        resolver = resolve.all_tutors
    )
    tutorUser= DjangoFilterConnectionField(
        TutorUsername,
        desciption = "A list of username of tutors",
        resolver = resolve.all_username
    )

