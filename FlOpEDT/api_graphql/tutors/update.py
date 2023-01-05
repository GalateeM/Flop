from graphene_django import DjangoObjectType
from people.models import Tutor
import graphene
from .types import TutorType
from django.db import models

class UpdateTutor(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        email = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()


    tutor = graphene.Field(TutorType)

    @classmethod
    def mutate(cls, root, info, username, **update_data):
        tutor = Tutor.objects.filter(username=username)
        if tutor:
            params = update_data
            tutor.update(**{k: v for k, v in params.items() if params[k]})
            return UpdateTutor(tutor=tutor.first())
        else:
            print('Tutor with given ID does not exist in the database')