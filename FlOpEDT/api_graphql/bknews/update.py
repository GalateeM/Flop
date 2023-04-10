import graphene
from graphql_relay import from_global_id

from displayweb.models import BreakingNews
from base.models import Department

from api_graphql import lib
from .types import BknewsType


class UpdateBknews(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        department = graphene.Argument(graphene.ID)
        week = graphene.Int()
        year = graphene.Int()
        x_beg = graphene.Float()
        x_end = graphene.Float()
        y = graphene.Int()
        txt = graphene.String()
        is_linked = graphene.String()
        fill_color = graphene.String()
        strk_color = graphene.String()

    bknews = graphene.Field(BknewsType)

    @classmethod
    def mutate(cls, root, info, id, **params):
        id = from_global_id(id) [1]
        bknews_set = BreakingNews.objects.filter(id=id)
        if bknews_set:
            lib.assign_value_to_foreign_key(params, "department", Department, "update")

            bknews_set.update(**params)
            bknews = bknews_set.first()
            bknews.save()

            return UpdateBknews(bknews=bknews)

        else:
            print('Breaking new with given ID does not exist in the database')