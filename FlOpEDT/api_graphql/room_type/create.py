import graphene
from base.models import Department, RoomType
from .types import RoomTypeNode
from graphql_relay import from_global_id
from api_graphql import lib

class CreateRoomType(graphene.Mutation):
    class Arguments:
        name = graphene.String(required = True)
        department = graphene.Argument(graphene.ID)

    room_types = graphene.Field(RoomTypeNode)

    @classmethod
    def mutate(cls,root,info, **params):

        #foreignkey

        lib.assign_value_to_foreign_key(params,"department", Department, "create")

        room_types = RoomType.objects.create(**params)
        return CreateRoomType(room_types)