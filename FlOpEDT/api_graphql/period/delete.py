import graphene
from graphql_relay import from_global_id

from base.models import Period

from .types import PeriodType


class DeletePeriod(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    period = graphene.Field(PeriodType)

    @classmethod
    def mutate(cls,root, info, id):
        id = from_global_id(id) [1]
        try:
            period = Period.objects.get(id=id)
            period.delete()

            return DeletePeriod(period)
        
        except Period.DoesNotExist:
            print("Period with given Id does not exist in the database")
