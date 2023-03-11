import graphene
from base.models import Room, Department, RoomType
from .types import RoomNode
from api_graphql.room_type.types import RoomTypeNode
from api_graphql.department.types import DepartmentType
from graphql_relay import from_global_id
from api_graphql import lib

class CreateRoom(graphene.Mutation):
    class Arguments:
        name = graphene.String(required = True)
        types = graphene.List(graphene.ID, required = True)                           
        subroom_of = graphene.List(graphene.ID)
        departments = graphene.List(graphene.ID, required = True)

    rooms = graphene.Field(RoomNode)
    types = graphene.List(RoomTypeNode)
    subroom_of = graphene.List(RoomNode)
    departments = graphene.List(DepartmentType)

    @classmethod
    def mutate(cls,root,info, **params):   

        #ManyToMany
        types = lib.get_manyToManyField_values(params, "types", RoomType)
        subroom_of = lib.get_manyToManyField_values(params, "subroom_of", Room)
        departments = lib.get_manyToManyField_values(params, "departments", Department)
        rooms = Room.objects.create(**params)
        
        lib.assign_values_to_manyToManyField(rooms, "types", types)
        lib.assign_values_to_manyToManyField(rooms, "subroom_of", subroom_of)
        lib.assign_values_to_manyToManyField(rooms, "departments", departments)
        rooms.save()

        return CreateRoom(rooms = rooms, types = rooms.types.all(), subroom_of = rooms.subroom_of.all(), departments = rooms.departments.all())        