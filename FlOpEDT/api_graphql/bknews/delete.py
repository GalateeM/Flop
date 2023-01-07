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
            bknews_set = BreakingNews.objects.filter(id=id)
            if bknews_set:
                bknews=bknews_set.first()
                bknews.delete()
                return DeleteBknews(bknews)
            else:
                print('Breaking new with given ID does not exist in the database')