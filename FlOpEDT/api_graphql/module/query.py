from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import ModuleNode

class Query(BaseQuery):
    modules = DjangoFilterConnectionField(
        ModuleNode,
        description="A list of modules.",
        resolver=resolve.all_modules
    )
    
