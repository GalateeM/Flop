import graphene
from graphql_relay import from_global_id

from base.models import RoomType

from .types import RoomTypeNode


class DeleteRoomType(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    room_types = graphene.Field(RoomTypeNode)


    @classmethod
    def mutate(cls, root, info, id):
        id = from_global_id(id) [1]
        try:
            room_types = RoomType.objects.get(id=id)
            room_types.delete()

            return DeleteRoomType(room_types)
        except RoomType.DoesNotExist:
            print("Room Type with the given Id does not exist in the database")