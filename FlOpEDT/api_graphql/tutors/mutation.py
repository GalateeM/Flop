from api_graphql.base import BaseMutation
from .create import CreateTutor
from .update import UpdateTutor
from .delete import DeleteTutor

class Mutation(BaseMutation):
    """
    This class contains the fields of models that are supposed to be 
    mutated.
    """
    create_tutor = CreateTutor.Field()
    update_tutor = UpdateTutor.Field()
    delete_tutor = DeleteTutor.Field()