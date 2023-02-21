from graphene_django import DjangoObjectType
from displayweb.models import BreakingNews
import graphene
from .types import BknewsType
from graphql_relay import from_global_id
from base.models import Department

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
            if params.get("department") != None:
                id_dept = from_global_id(params["department"])[1]
                params["department"] = id_dept

            bknews_set.update(**params)
            bknews = bknews_set.first()
            bknews.save()

            return UpdateBknews(bknews=bknews)

        else:
            print('Breaking new with given ID does not exist in the database')