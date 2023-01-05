from api_graphql.base import BaseMutation
from .create import createTutor
from .update import UpdateTutor

class Mutation(BaseMutation):
    """
    This class contains the fields of models that are supposed to be 
    mutated.
    """
    create_tutor = createTutor.Field()
    update_tutor = UpdateTutor.Field()