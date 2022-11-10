from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import ScheduledCourseNode

class Query(BaseQuery):
    scheduledCourses = DjangoFilterConnectionField(
        ScheduledCourseNode,
        description="A list of scheduled courses.",
        resolver=resolve.all_scheduled_courses
    )
    
