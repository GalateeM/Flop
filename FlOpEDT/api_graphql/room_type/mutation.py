from api_graphql.base import BaseMutation
from .create import CreateRoomType
from .update import UpdateRoomType
from .delete import DeleteRoomType

class Mutation(BaseMutation):
    create_room_type = CreateRoomType.Field()
    update_room_type = UpdateRoomType.Field()
    delete_room_type = DeleteRoomType.Field()