import graphene
from base.models import GenericGroup
from .types import GenericGroupNode
from graphql_relay import from_global_id

class CreateGenericGroup(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        train_prog = graphene.Argument(graphene.ID)
        type = graphene.Argument