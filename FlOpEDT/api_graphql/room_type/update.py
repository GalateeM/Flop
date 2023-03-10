import graphene
from base.models import Department, RoomType
from .types import RoomTypeNode
from graphql_relay import from_global_id
from api_graphql import lib

class UpdateRoomType(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(graphene.ID)
        department = graphene.Argument(graphene.ID)


    room_types = graphene.Field(RoomTypeNode)

    @classmethod
    def mutate(cls, root, info,id, **params):
        id = from_global_id(id)[1]
        room_type_set = RoomType.objects.filter(id=id)

        if room_type_set:

            #foreignkey

            lib.assign_value_to_foreign_key(params, "department", Department, "update")

            room_type_set.update(**params)
            room_types = room_type_set.first()
            room_types.save()

            return UpdateRoomType(room_types)
        else:
            print("Room Type with the given ID does not exist in the database")

