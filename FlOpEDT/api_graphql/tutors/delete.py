from graphene_django import DjangoObjectType
import graphene
from people.models import Tutor
from .types import TutorType
from graphql_relay import from_global_id

class DeleteTutor(graphene.Mutation):
        class Arguments:
            id = graphene.ID()

        tutor = graphene.Field(TutorType)

        @classmethod
        def mutate(cls, root, info, id):
            _, object_id = from_global_id(id)
            tutor = Tutor.objects.get(id=object_id)
            tutor.delete()
            return DeleteTutor(tutor)