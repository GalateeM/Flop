from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError

from api_graphql.base import BaseQuery
from .types import UnscheduledCourseNode


class Query(BaseQuery):
    unscheduled_courses = DjangoFilterConnectionField(UnscheduledCourseNode)

    def resolve_unscheduled_courses(self, info, **kwargs):
        queryset = UnscheduledCourseNode.get_queryset(info)
        filterset_class = UnscheduledCourseNode.get_filter(info)
        filterset = filterset_class(data=kwargs, queryset=queryset, request=info.context)
        if not filterset.is_valid():
            raise GraphQLError('Invalid input')
        return filterset.qs