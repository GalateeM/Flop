import graphene
from base.models import Room, Department, RoomType
from .types import RoomNode
from graphql_relay import from_global_id


class DeleteRoom(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    rooms = graphene.Field(RoomNode)

    @classmethod
    def mutate(cls, root, info, id):
        id = from_global_id(id) [1]
        try:
            rooms = Room.objects.get(id=id)
            rooms.delete()
            return DeleteRoom(rooms)
        except Room.DoesNotExist:
            print('Room with given ID does not exist in the database')