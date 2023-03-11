import graphene
from graphql_relay import from_global_id

from base.models import UserPreference

from .types import UserPreferenceNode


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