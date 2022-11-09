from graphene import List, Int, Field
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import DepartmentNode, TrainingProgrammeQL, DummyDictNode

class Query(BaseQuery):
    departments = DjangoFilterConnectionField(
        DepartmentNode,
        description="A list of departments.",
        resolver=resolve.all_departments
    )
    training_programmes = List(
        lambda: TrainingProgrammeQL,
        description="A list of training programmes.",
        week_nb=Int(required=True),
        week_yy=Int(required=True),
        resolver=resolve.all_training_programmes
    )
    dictionary = Field(DummyDictNode,
                description='Get a dummy dictionary.',
                resolver=resolve.resolve_dic)

