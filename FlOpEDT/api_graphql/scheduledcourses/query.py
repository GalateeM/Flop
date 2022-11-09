from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import CourseNode

class Query(BaseQuery):
    courses = DjangoFilterConnectionField(
        CourseNode,
        description="A list of scheduled courses.",
        resolver=resolve.all_courses
    )
    