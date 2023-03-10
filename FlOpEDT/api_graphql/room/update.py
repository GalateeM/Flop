import graphene
from base.models import Room, Department, RoomType
from .types import RoomNode
from graphql_relay import from_global_id
from api_graphql import lib

class UpdateRoom(graphene.Mutation):
    class arguments:
        id = graphene.ID(required=True)
        department = graphene.List(graphene.ID, required = True)
        name = graphene.String(required=True)
        types = graphene.List(graphene.ID, required = True)                           
        subroom_of = graphene.List(graphene.ID, required = True)
    
    rooms = graphene.Field(RoomNode)

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
            lib.assign_values_to_manyToManyField_values(params, "types", types)
            lib.assign_values_to_manyToManyField_values(params, "subroom_of", subroom_of)
            lib.assign_values_to_manyToManyField_values(params, "departments", departments)
            rooms.save()

            return UpdateRoom(rooms)
        else:
            print("Room with the given ID does not exist")


      
        
