from graphene import relay
from graphene_django import DjangoObjectType
from base.models import GroupType
from.filter import GroupTypeFilter
from graphql_relay import from_global_id

class GroupTypeNode(DjangoObjectType):
    class Meta:
        model = GroupType
        filterset_class = GroupTypeFilter
        interfaces = (relay.Node, )