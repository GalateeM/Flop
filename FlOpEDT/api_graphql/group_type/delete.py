from graphene_django import DjangoObjectType
import graphene
from django.db import models
from .types import GroupTypeNode
from base.models import Department, GroupType
from graphql_relay import from_global_id
from api_graphql import lib

class DeleteGroupType(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)

    group_type = graphene.Field(GroupTypeNode)   

    @classmethod
    def mutate(cls,root,info, id):
        id = from_global_id(id) [1]
        try:
            group_type = GroupType.objects.get(id=id)
            group_type.delete()            
            return DeleteGroupType(group_type=group_type)
        
        except GroupType.DoesNotExist:
            print("Groupe type with given ID does not exist in the database")