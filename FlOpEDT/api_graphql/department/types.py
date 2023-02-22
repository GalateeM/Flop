from graphene import relay
from graphene_django import DjangoObjectType
from base.models import Department
from .filter import DepartmentFilter
from graphql_relay import from_global_id

class DepartmentType(DjangoObjectType):
    class Meta:
        model = Department
        filterset_class = DepartmentFilter
        interfaces = (relay.Node, )