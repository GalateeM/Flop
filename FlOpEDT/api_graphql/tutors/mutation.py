from api_graphql.base import BaseMutation
from .create import createTutor

class Mutation(BaseMutation):
    """
    This class contains the fields of models that are supposed to be 
    mutated.
    """
    create_tutor = createTutor.Field()