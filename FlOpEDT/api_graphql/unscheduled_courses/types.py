from graphene import relay
from graphene_django import DjangoObjectType

from base.models import Course

from .filter import UnscheduledCourseFilter


class UnscheduledCourseNode(DjangoObjectType):
    class Meta:
        model = Course
        filterset_class = UnscheduledCourseFilter
        interfaces = (relay.Node, )