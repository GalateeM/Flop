import graphene
from base.models import Room, Department, RoomType
from .types import RoomNode
from graphql_relay import from_global_id
from api_graphql import lib

class CreateRoom(graphene.Mutation):
    class Arguments:
        name = graphene.String(graphene.ID, required = True)
        types = graphene.List(graphene.ID, required = True)                           
        subroom_of = graphene.List(graphene.ID, required = True)
        departments = graphene.List(graphene.ID, required = True)

    room = graphene.Field(RoomNode)

    @classmethod
    def mutate(cls,root,info, **params):   

        #ManyToMany

        types = lib.get_manyToManyField_values(params, "types", RoomType)
        subroom_of = lib.get_manyToManyField_values(params, "subroom_of", Room)
        departments = lib.get_manyToManyField_values(params, "departments", Department)

        rooms = Room.objects.create(**params)

        lib.assign_values_to_manyToManyField_values(params, "types", types)
        lib.assign_values_to_manyToManyField_values(params, "subroom_of", subroom_of)
        lib.assign_values_to_manyToManyField_values(params, "departments", departments)
        rooms.save()

        return CreateRoom(rooms)

        