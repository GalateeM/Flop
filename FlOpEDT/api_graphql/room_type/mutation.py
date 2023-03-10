from api_graphql.base import BaseMutation
from .create import CreateRoomType
from .update import UpdateRoomType
from .delete import DeleteRoomType

class Mutation(BaseMutation):
    
    """
     This class contains the fields of models that are supposed to be 
     mutated.
     """

    create_room_type = CreateRoomType.Field()
    update_room_type = UpdateRoomType.Field()
    delete_room_type = DeleteRoomType.Field()

