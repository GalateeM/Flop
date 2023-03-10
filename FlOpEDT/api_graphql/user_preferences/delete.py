from graphene_django import DjangoObjectType
import graphene
from django.db import models
from base.models import Week, UserPreference
from people.models import Tutor
from .types import UserPreferenceNode
from graphql_relay import from_global_id
from api_graphql import lib

class DeleteUserPreference(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    
    user_preference = graphene.Field(UserPreferenceNode)

    @classmethod
    def mutate(cls,root, info, id):
        id = from_global_id(id) [1]
        try:
            user_preference = UserPreference.objects.get(id=id)
            user_preference.delete()
            return DeleteUserPreference(user_preference)
        
        except UserPreference.DoesNotExist:
            print('User preference with given ID does not exist in the database')