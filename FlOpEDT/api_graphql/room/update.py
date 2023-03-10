import graphene
from base.models import Room, Department, RoomType
from api_graphql.room_type.types import RoomTypeNode
from api_graphql.department.types import DepartmentType
from .types import RoomNode
from graphql_relay import from_global_id
from api_graphql import lib

class UpdateRoom(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        types = graphene.List(graphene.ID)                           
        subroom_of = graphene.List(graphene.ID)
        departments = graphene.List(graphene.ID)
    
    rooms = graphene.Field(RoomNode)
    types = graphene.List(RoomTypeNode)
    subroom_of = graphene.List(RoomNode)
    departments = graphene.List(DepartmentType)

    @classmethod
    def mutate(cls, root, info, id, **params):
        id = from_global_id(id) [1]
        rooms_set = Room.objects.filter(id=id)
        if rooms_set:

            #manytomany

            types = lib.get_manyToManyField_values(params, "types", RoomType)
            subroom_of = lib.get_manyToManyField_values(params, "subroom_of", Room)
            departments = lib.get_manyToManyField_values(params, "departments", Department)

            rooms_set.update(**params)
            rooms = rooms_set.first()
            lib.assign_values_to_manyToManyField(rooms, "types", types)
            lib.assign_values_to_manyToManyField(rooms, "subroom_of", subroom_of)
            lib.assign_values_to_manyToManyField(rooms, "departments", departments)
            rooms.save()

            return UpdateRoom(rooms = rooms, types = rooms.types.all(), subroom_of = rooms.subroom_of.all(), departments = rooms.departments.all())
        else:
            print("Room with the given ID does not exist")


      
        
