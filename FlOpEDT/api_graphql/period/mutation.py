from api_graphql.base import BaseMutation
from .create import CreatePeriod
from .update import UpdatePeriod
from .delete import DeletePeriod

class Mutation(BaseMutation):
    """
    This class contains the fields of models that are supposed to be 
    mutated.
    """

    create_period = CreatePeriod.Field()
    update_period = UpdatePeriod.Field()
    delete_period = DeletePeriod.Field()
