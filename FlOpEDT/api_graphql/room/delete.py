import graphene
from base.models import Room
from .types import RoomNode
from graphql_relay import from_global_id

class DeleteRoom(graphene.Mutation):
    class arguments:
        id = graphene.ID(required=True)

    rooms = graphene.Field(RoomNode)

    @classmethod
    def mutate(cls, root, info, id):
        id = from_global_id(id) [1]
        try:
            rooms = Room.objects.get(id=id)
            rooms.delete
            return DeleteRoom(rooms)
        except Room.DoesNotExist:
            print('Breaking new with given ID does not exist in the database')