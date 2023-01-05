from graphene_django import DjangoObjectType
import graphene
from people.models import Tutor
from .types import TutorType

class DeleteTutor(graphene.Mutation):
        class Arguments:
            # id = graphene.ID()
            username = graphene.String()

        tutor = graphene.Field(TutorType)

        @classmethod
        def mutate(cls, root, info, username):
            tutor = Tutor.objects.get(username=username)
            tutor.delete()
            return DeleteTutor(tutor)