import graphene
from base.models import Room, Department
from .types import RoomNode
from graphql_relay import from_global_id

class UpdateRoom(graphene.Mutation):
    class arguments:
        id = graphene.ID(required=True)
        department = graphene.Argument(graphene.ID)
        name = graphene.String(required=True)
    
    rooms = graphene.Field(RoomNode)

    @classmethod
    def mutate(cls, root, info, id, **params):
        id = from_global_id(id) [1]
        rooms_set = Room.objects.filter(id=id)
        if rooms_set:
            if params.get("department") != None:
                id_dept = from_global_id(params["department"]) [1]
                params["department"] = id_dept
            
            rooms_set.update(**params)
            rooms = rooms_set.first()
            rooms.save()

            return UpdateRoom(romms=rooms)
        
        else:
            print('Breaking new with given ID does not exist in the database')
        
