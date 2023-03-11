from api_graphql.base import BaseMutation
from .create import CreateRoom
from .update import UpdateRoom
from .delete import DeleteRoom

class Mutation(BaseMutation):
    create_room = CreateRoom.Field()
    update_room = UpdateRoom.Field()
    delete_room = DeleteRoom.Field()