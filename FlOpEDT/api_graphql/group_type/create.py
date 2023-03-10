from graphene_django import DjangoObjectType
import graphene
from django.db import models
from .types import GroupTypeNode
from base.models import Department, GroupType
from graphql_relay import from_global_id
from api_graphql import lib

class CreateGroupType(graphene.Mutation):
    class Arguments:
        name = graphene.String(required = True)
        department = graphene.Argument(graphene.ID)

    group_type = graphene.Field(GroupTypeNode)   

    @classmethod
    def mutate(cls,root,info, **params):
        # foreignKey  
        lib.assign_value_to_foreign_key(params, "department", Department, "create")
        
        group_type = GroupType.objects.create(**params)
        
        return CreateGroupType(group_type=group_type)