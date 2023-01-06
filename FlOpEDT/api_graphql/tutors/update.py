from graphene_django import DjangoObjectType
from people.models import Tutor
import graphene
from .types import TutorType
from graphql_relay import from_global_id

class UpdateTutor(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        username = graphene.String()
        email = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()


    tutor = graphene.Field(TutorType)

    @classmethod
    def mutate(cls, root, info, id, **update_data):
        _, object_id = from_global_id(id)
        tutor = Tutor.objects.filter(id=object_id)
        if tutor:
            params = update_data
            tutor.update(**{k: v for k, v in params.items() if params[k]})
            return UpdateTutor(tutor=tutor.first())
        else:
            print('Tutor with given ID does not exist in the database')