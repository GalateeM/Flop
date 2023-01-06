from graphene_django import DjangoObjectType
import graphene
from displayweb.models import BreakingNews
from .types import BknewsType
from graphql_relay import from_global_id

class DeleteBknews(graphene.Mutation):
        class Arguments:
            id = graphene.ID()

        bknews = graphene.Field(BknewsType)

        @classmethod
        def mutate(cls, root, info, id):
            _, object_id = from_global_id(id)
            bknews = BreakingNews.objects.get(id=object_id)
            bknews.delete()
            return DeleteBknews(bknews)