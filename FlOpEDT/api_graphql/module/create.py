from graphene_django import DjangoObjectType
import graphene
from django.db import models
from .types import ModuleNode
from base.models import Module, TrainingProgramme, Period
from people.models import Tutor
from graphql_relay import from_global_id
from api_graphql import lib

class CreateModule(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        abbrev = graphene.String(required = True)
        head = graphene.Argument(graphene.ID)
        ppn = graphene.String()
        train_prog = graphene.Argument(graphene.ID, required = True)
        period = graphene.Argument(graphene.ID, required = True)
        url = graphene.String()
        description = graphene.String()

    module = graphene.Field(ModuleNode)
    
    @classmethod
    def mutate(cls, root, info, **params):
        # Foreign keys
        lib.assign_value_to_foreign_key(params, "head", Tutor, "create")
        lib.assign_value_to_foreign_key(params, "train_prog", TrainingProgramme, "create")
        lib.assign_value_to_foreign_key(params, "period", Period, "create")
        
        module = Module.objects.create(**params)
        
        return CreateModule(module = module)