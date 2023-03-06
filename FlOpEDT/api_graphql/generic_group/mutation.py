from api_graphql.base import BaseMutation
from .create import CreateGenericGroup
from .update import UpdateGenericGroup
from .delete import DeleteGenericGroup

class Mutation(BaseMutation):
    create_generic_group = CreateGenericGroup.Field()
    update_generic_group = UpdateGenericGroup.Field()
    delete_generic_group = DeleteGenericGroup.Field()