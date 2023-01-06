from graphene_django import DjangoObjectType
import graphene
from django.db import models
from people.models import Tutor
from .types import TutorType
from .query import Query

class CreateTutor(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        email = graphene.String() 
        first_name = graphene.String()
        last_name = graphene.String()

    tutor = graphene.Field(TutorType)

    @classmethod
    def mutate(cls, root, info, **user_data):
        tutor = Tutor(
            first_name=user_data.get('first_name'),
            username=user_data.get('username'),
            email=user_data.get('email'),
        )
        
        tutor.save()
        return CreateTutor(tutor=tutor)