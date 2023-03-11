from api_graphql.base import BaseMutation
from .create import CreateTutor
from .update import UpdateTutor
from .delete import DeleteTutor

class Mutation(BaseMutation):
    create_tutor = CreateTutor.Field()
    update_tutor = UpdateTutor.Field()
    delete_tutor = DeleteTutor.Field()