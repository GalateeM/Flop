from graphene import relay
from graphene_django import DjangoObjectType

from base.models import Course

from .filter import CourseFilter


class CourseNode(DjangoObjectType):
    class Meta:
        model = Course
        filterset_class = CourseFilter
        interfaces = (relay.Node, )