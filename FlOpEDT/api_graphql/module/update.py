import graphene
from graphql_relay import from_global_id

from base.models import Module, TrainingProgramme, Period
from people.models import Tutor

from api_graphql import lib
from .types import ModuleNode


class UpdateModule(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
        name = graphene.String()
        abbrev = graphene.String()
        head = graphene.Argument(graphene.ID)
        ppn = graphene.String()
        train_prog = graphene.Argument(graphene.ID)
        period = graphene.Argument(graphene.ID)
        url = graphene.String()
        description = graphene.String()

    module = graphene.Field(ModuleNode)

    @classmethod
    def mutate(cls, root, info, id, **params):
        id = from_global_id(id)[1]
        module_set = Module.objects.filter(id = id)
        if module_set:
            lib.assign_value_to_foreign_key(params, "head", Tutor, "create")
            lib.assign_value_to_foreign_key(params, "train_prog", TrainingProgramme, "create")
            lib.assign_value_to_foreign_key(params, "period", Period, "create")

            module_set.update(**params)
            module = module_set.first()
            module.save()

            return UpdateModule(module = module)
        else:
            print('Group Type with given ID does not exist in the database')