import graphene
from graphql_relay import from_global_id

from base.models import Module

from .types import ModuleNode


class DeleteModule(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)

    module = graphene.Field(ModuleNode)

    @classmethod
    def mutate(cls, root, info, id):
        id = from_global_id(id) [1]
        try:
            module = Module.objects.get(id = id)
            module.delete()
            return DeleteModule(module)

        except Module.DoesNotExist:
            print('Module with given ID does not exist in the database')