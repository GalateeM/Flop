import graphene

from base.models import Week, UserPreference
from people.models import Tutor

from api_graphql import lib
from .types import UserPreferenceNode


class CreateUserPreference(graphene.Mutation):
    class Arguments:
        user = graphene.Argument(graphene.ID, required = True)
        week = graphene.Argument(graphene.ID, required = True)
        day = graphene.String()
        start_time = graphene.Int(required = True)
        duration = graphene.Int()
        value = graphene.Int()

    user_preference = graphene.Field(UserPreferenceNode)

    @classmethod
    def mutate(cls,root,info, **params):
        lib.assign_value_to_foreign_key(params, "user", Tutor, "create")
        lib.assign_value_to_foreign_key(params, "week", Week, "create")
        
        user_preference = UserPreference.objects.create(**params)
        
        return CreateUserPreference(user_preference)