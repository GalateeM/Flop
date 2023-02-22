import graphene
from people.models import Tutor
from .types import TutorType
from graphql_relay import from_global_id

class DeleteTutor(graphene.Mutation):
        class Arguments:
            id = graphene.ID(required=True)

        tutor = graphene.Field(TutorType)

        @classmethod
        def mutate(cls, root, info, id):
            id = from_global_id(id) [1]
            try:
                tutor = Tutor.objects.get(id=id)
                tutor.delete()
                return DeleteTutor(tutor)
            
            except Tutor.DoesNotExist:
                print('Tutor with given ID does not exist in the database')