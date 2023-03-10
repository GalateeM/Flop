from api_graphql.base import BaseMutation
from .create import CreateWeek
from .update import UpdateWeek
from .delete import DeleteWeek

class Mutation(BaseMutation):
    
    """
     This class contains the fields of models that are supposed to be 
     mutated.
     """

    create_week = CreateWeek.Field()
    update_week = UpdateWeek.Field()
    delete_week = DeleteWeek.Field()