from api_graphql.base import BaseMutation
from .create import CreateUserPreference
from .update import UpdateUserPreference
from .delete import DeleteUserPreference

class Mutation(BaseMutation):
    create_user_preference = CreateUserPreference.Field()
    update_user_preference = UpdateUserPreference.Field()
    delete_user_preference = DeleteUserPreference.Field()