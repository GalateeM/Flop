from graphene_django import DjangoObjectType
from displayweb.models import BreakingNews
import graphene
from .types import BknewsType
from graphql_relay import from_global_id
from api_graphql.department.types import DepartmentType

class UpdateBknews(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        week = graphene.Int()
        year = graphene.Int()
        txt = graphene.String()
        #department = graphene.Field(DepartmentType)
        x_beg = graphene.Float()
        x_end = graphene.Float()
        y = graphene.Int()
        is_linked = graphene.String()
        fill_color = graphene.String()
        strk_color = graphene.String()

    bknews = graphene.Field(BknewsType)

    @classmethod
    def mutate(cls, root, info, id, **user_data):
        _, object_id = from_global_id(id)
        bknews = BreakingNews.objects.filter(id=object_id)
        if bknews:
            params = user_data
            bknews.update(**{k: v for k, v in params.items() if params[k]})
            return UpdateBknews(bknews=bknews.first())
        else:
            print('Breaking new with given ID does not exist in the database')