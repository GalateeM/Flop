import graphene
from displayweb.models import BreakingNews
from base.models import Department
from .types import BknewsType
from graphql_relay import from_global_id

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
        print("yo")
        department = None
        if params.get("department") != None:
            id = from_global_id(params["department"])[1]
            department = Department.objects.get(id=id)
            del params["department"]

        bknews = BreakingNews.objects.create(**params)
        bknews.department = department
        bknews.save()

        return CreateBknews(bknews=bknews)