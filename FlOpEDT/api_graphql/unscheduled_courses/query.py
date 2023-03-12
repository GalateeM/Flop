from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from .types import UnscheduledCourseNode


class Query(BaseQuery):
    unscheduled_courses = DjangoFilterConnectionField(UnscheduledCourseNode)