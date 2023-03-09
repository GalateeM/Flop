import graphene
from base.models import GenericGroup, TrainingProgramme, GroupType
from .types import GenericGroupNode
from graphql_relay import from_global_id
from api_graphql import lib

class UpdateGenericGroup(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        train_prog = graphene.Argument(graphene.ID)
        type = graphene.Argument(graphene.ID)
        size = graphene.Int()
    
    generic_group = graphene.Field(GenericGroupNode)

    @classmethod
    def mutate(cls, root, info, id, **params):
        id = from_global_id(id)[1]
        generic_group_set = GenericGroup.objects.filter(id=id)
        if generic_group_set:
            # foreign key
            lib.assign_value_to_foreign_key(params, "train_prog", TrainingProgramme, "update")
            lib.assign_value_to_foreign_key(params, "type", GroupType , "update")

            generic_group_set.update(**params)
            generic_group = generic_group_set.first()
            generic_group.save()

            return UpdateGenericGroup(generic_group=generic_group)
        else:
            print("Generic group with given ID does not exist in the database")