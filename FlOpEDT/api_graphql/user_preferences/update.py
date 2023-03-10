from graphene_django import DjangoObjectType
import graphene
from django.db import models
from base.models import Week, UserPreference
from people.models import Tutor
from .types import UserPreferenceNode
from graphql_relay import from_global_id
from api_graphql import lib

class UpdateUserPreference(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
        user = graphene.Argument(graphene.ID)
        week = graphene.Argument(graphene.ID)
        day = graphene.String()
        start_time = graphene.Int()
        duration = graphene.Int()
        value = graphene.Int()
    
    user_preference = graphene.Field(UserPreferenceNode)

    @classmethod
    def mutate(cls, root, info, id, **params):
        id = from_global_id(id)[1]
        user_preference_set = UserPreference.objects.filter(id=id)
        if user_preference_set:
            lib.assign_value_to_foreign_key(params, "user", Tutor, "create")
            lib.assign_value_to_foreign_key(params, "week", Week, "create")

            user_preference_set.update(**params)
            user_preference = user_preference_set.first()

            return UpdateUserPreference(user_preference)
        else:
            print('User preference with given ID does not exist in the database')