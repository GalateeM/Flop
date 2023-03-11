from api_graphql.base import BaseMutation
from .create import CreatePeriod
from .update import UpdatePeriod
from .delete import DeletePeriod

class Mutation(BaseMutation):
    create_period = CreatePeriod.Field()
    update_period = UpdatePeriod.Field()
    delete_period = DeletePeriod.Field()