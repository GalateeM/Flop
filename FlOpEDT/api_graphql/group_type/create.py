import graphene

from base.models import Department, GroupType

from api_graphql import lib
from .types import GroupTypeNode


class CreateGroupType(graphene.Mutation):
    class Arguments:
        name = graphene.String(required = True)
        department = graphene.Argument(graphene.ID)

    group_type = graphene.Field(GroupTypeNode)   

    @classmethod
    def mutate(cls,root,info, **params):
        lib.assign_value_to_foreign_key(params, "department", Department, "create")
        
        group_type = GroupType.objects.create(**params)
        
        return CreateGroupType(group_type=group_type)