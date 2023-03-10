from graphene_django import DjangoObjectType
import graphene
from django.db import models
from base.models import TrainingProgramme, Department
from .types import TrainingProgrammeType
from api_graphql import lib

class CreateTrainingProgramme(graphene.Mutation):
    class Arguments:
        name = graphene.String(required = True)
        abbrev = graphene.String(required = True)
        department = graphene.Argument(graphene.ID)
    
    training_programme = graphene.Field(TrainingProgrammeType)

    @classmethod
    def mutate(cls, root, info, **params):
        lib.assign_value_to_foreign_key(params, "department", Department, "create")

        training_programme = TrainingProgramme.objects.create(**params)

        return CreateTrainingProgramme(training_programme)