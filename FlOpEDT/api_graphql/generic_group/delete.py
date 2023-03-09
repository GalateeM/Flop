import graphene
from base.models import GenericGroup, TrainingProgramme
from .types import GenericGroupNode
from graphql_relay import from_global_id
from api_graphql import lib

class DeleteGenericGroup(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    generic_group = graphene.Field(GenericGroupNode)
    
    @classmethod
    def mutate(cls,root, info, id):
        id = from_global_id(id) [1]
        try:
            generic_group = GenericGroup.objects.get(id=id)
            generic_group.delete()
            return DeleteGenericGroup(generic_group)
        
        except GenericGroup.DoesNotExist:
            print('Generic group with given ID does not exist in the database')