from api_graphql.base import BaseMutation
from .create import CreateUserPreference
from .update import UpdateUserPreference
from .delete import DeleteUserPreference

class Mutation(BaseMutation):
    
    """
     This class contains the fields of models that are supposed to be 
     mutated.
     """

    create_user_preference = CreateUserPreference.Field()
    update_user_preference = UpdateUserPreference.Field()
    delete_user_preference = DeleteUserPreference.Field()