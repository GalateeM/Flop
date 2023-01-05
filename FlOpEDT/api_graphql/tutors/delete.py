from graphene_django import DjangoObjectType
from people.models import Tutor
from .filter import TutorFilter

class DeleteTutor(graphene.Mutation):
        class Arguments:
            id = graphene.ID()

        Tutor = graphene.Field(TutorType)

        @classmethod
        def mutate(cls, root, info, id):
            Tutor = TUTOR.objects.get(id=id)
            Tutor.delete()
            return DeleteTutor(Tutor)