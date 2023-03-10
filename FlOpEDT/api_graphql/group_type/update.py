from graphene_django import DjangoObjectType
import graphene
from django.db import models
from .types import GroupTypeNode
from base.models import Department, GroupType
from graphql_relay import from_global_id
from api_graphql import lib

class UpdateGroupType(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
        name = graphene.String()
        department = graphene.Argument(graphene.ID)

    group_type = graphene.Field(GroupTypeNode)   

    @classmethod
    def mutate(cls,root,info, id, **params):
        id = from_global_id(id) [1]
        group_type_set = GroupType.objects.filter(id = id)
        if group_type_set:
            # foreignKey
            lib.assign_value_to_foreign_key(params, "department", Department, "create")
            
            group_type_set.update(**params)
            group_type = group_type_set.first()
            
            return UpdateGroupType(group_type=group_type)
        else:
            print("Groupe type with given ID does not exist in the database")