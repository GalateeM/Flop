from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import CourseTypeNode

class Query(BaseQuery):
    courseTypes = DjangoFilterConnectionField(
        CourseTypeNode,
        description = "A list of course types",
        resolver = resolve.all_course_type
    )
