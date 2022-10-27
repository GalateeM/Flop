from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

#from ..base import BaseQuery
from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import DepartmentNode, TrainingProgrammeQL

class Query(BaseQuery):
    departments = DjangoFilterConnectionField(
        DepartmentNode,
        description="A list of departments.",
        resolver=resolve.all_departments
    )
    training_programmes = List(
        lambda: TrainingProgrammeQL,
        description="A list of training programmes.",
        resolver=resolve.all_training_programmes
    )
    
