from graphene_django import DjangoObjectType
import graphene
from django.db import models
from base.models import Week, UserPreference
from people.models import Tutor
from .types import UserPreferenceNode
from graphql_relay import from_global_id
from api_graphql import lib

class CreateUserPreference(graphene.Mutation):
    class Arguments:
        user = graphene.Argument(graphene.ID, required = True)
        week = graphene.Argument(graphene.ID, required = True)
        day = graphene.String()
        start_time = graphene.Int()
        duration = graphene.Int()
        value = graphene.Int()

    user_preference = graphene.Field(UserPreferenceNode)

    @classmethod
    def mutate(cls,root,info, **params):
        lib.assign_value_to_foreign_key(params, "user", Tutor, "create")
        lib.assign_value_to_foreign_key(params, "week", Week, "create")
        
        user_preference = UserPreference.objects.create(**params)
        
        return CreateUserPreference(user_preference)