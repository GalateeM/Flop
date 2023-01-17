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
    
    @classmethod
    def get_group_types(cls, group_types_ids):
        group_types_ids = [ from_global_id(id)[1] for id in group_types_ids]
        return GroupType.objects.filter(id__in=group_types_ids)
