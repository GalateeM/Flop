from graphene_django import DjangoObjectType
import graphene
from django.db import models
from .types import ModuleNode
from base.models import Module, TrainingProgramme, Period
from people.models import Tutor
from graphql_relay import from_global_id
from api_graphql import lib

class DeleteModule(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)

    module = graphene.Field(Module)

    @classmethod
    def mutate(cls, root, info, id):
        id = from_global_id(id) [1]
        try:
            module = Module.objects.get(id = id)
            module.delete()
            return DeleteModule(module)

        except Module.DoesNotExist:
            print('Module with given ID does not exist in the database')