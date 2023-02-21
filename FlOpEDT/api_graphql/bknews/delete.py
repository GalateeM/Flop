import graphene
from displayweb.models import BreakingNews
from .types import BknewsType
from graphql_relay import from_global_id

class DeleteBknews(graphene.Mutation):
        class Arguments:
            id = graphene.ID(required=True)

        bknews = graphene.Field(BknewsType)

        @classmethod
        def mutate(cls, root, info, id):
            id = from_global_id(id) [1]
            try:
                bknews = BreakingNews.objects.get(id=id)
                bknews.delete()
                return DeleteBknews(bknews)
            except BreakingNews.DoesNotExist:
                print('Breaking new with given ID does not exist in the database')