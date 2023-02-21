import graphene
from base.models import Room, Department
from .types import RoomNode
from graphql_relay import from_global_id

class CreateRoom(graphene.Mutation):
    class arguments:
        department = graphene.Argument(graphene.ID)
        name = graphene.String(required=True)

    rooms = graphene.Field(RoomNode)

    @classmethod
    def mutate(cls, root, info, **params):
        department = None
        if params.get("department") != None:
            id = from_global_id(params["department"]) [1]
            department = Department.objects.get(id=id)
            del params["department"]
        rooms = Room.objects.create(**params)
        rooms.department = department
        rooms.save()

        return CreateRoom(rooms=rooms)