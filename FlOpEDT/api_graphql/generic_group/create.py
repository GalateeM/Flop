import graphene
from base.models import GenericGroup, TrainingProgramme, GroupType
from .types import GenericGroupNode
from graphql_relay import from_global_id
from api_graphql import lib

class CreateGenericGroup(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        train_prog = graphene.Argument(graphene.ID, required = True)
        type = graphene.Argument(graphene.ID)
        size = graphene.Int(required=True)
    
    generic_group = graphene.Field(GenericGroupNode)
    
    @classmethod
    def mutate(cls, root, info, **params):
        # foreign key
        lib.assign_value_to_foreign_key(params, "train_prog", TrainingProgramme, "create")
        lib.assign_value_to_foreign_key(params, "type", GroupType , "create")

        generic_group = GenericGroup.objects.create(**params)

        return CreateGenericGroup(generic_group = generic_group)