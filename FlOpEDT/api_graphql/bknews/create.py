import graphene
from displayweb.models import BreakingNews
from base.models import Department
from .types import BknewsType
from graphql_relay import from_global_id
from api_graphql import lib

class CreateBknews(graphene.Mutation):
    class Arguments:
        department = graphene.Argument(graphene.ID)
        week = graphene.Int()
        year = graphene.Int(required=True)
        x_beg = graphene.Float()
        x_end = graphene.Float()
        y = graphene.Int()
        txt = graphene.String(required=True)
        is_linked = graphene.String()
        fill_color = graphene.String()
        strk_color = graphene.String()

    bknews = graphene.Field(BknewsType)

    @classmethod
    def mutate(cls, root, info, **params):
        # foreign keys
        lib.assign_value_to_foreign_key(params, "department", Department, "create")
        # #############

        bknews = BreakingNews.objects.create(**params)

        return CreateBknews(bknews=bknews)