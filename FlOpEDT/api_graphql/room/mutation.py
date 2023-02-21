from api_graphql.base import BaseMutation
from .create import CreateRoom
from .update import UpdateRoom
from .delete import DeleteRoom

class Mutation(BaseMutation):

    create_rooms = CreateRoom.Field()
    update_rooms = UpdateRoom.Field()
    delete_rooms = DeleteRoom.Field()