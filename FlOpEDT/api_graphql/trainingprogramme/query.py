from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import TrainingProgrammeType

class Query(BaseQuery):
    trainingprogrammes = DjangoFilterConnectionField(
        TrainingProgrammeType,
        description="A list of trainingprogrammes.",
        resolver=resolve.all_trainingprogramme
    )
