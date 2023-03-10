from api_graphql.base import BaseMutation
from .create import CreateGroupType
from .update import UpdateGroupType
from .delete import DeleteGroupType

class Mutation(BaseMutation):
    create_group_type = CreateGroupType.Field()
    update_group_type = UpdateGroupType.Field()
    delete_group_type = DeleteGroupType.Field()