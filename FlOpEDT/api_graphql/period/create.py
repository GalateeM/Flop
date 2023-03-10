from graphene_django import DjangoObjectType
import graphene
from django.db import models
from .types import PeriodType
from base.models import Period, Department 
from api_graphql import lib
from graphql_relay import from_global_id

class CreatePeriod(graphene.Mutation):
    class Arguments:
        name = graphene.String(graphene.ID, required = True)
        department =graphene.Argument(graphene.ID)
        starting_week = graphene.Int(graphene.ID, required=True)
        ending_week = graphene.Int(graphene.ID, required = True)


    period = graphene.Field(PeriodType)

    @classmethod
    def mutate(cls, root, info, **params):
       
        #foreignKey
        lib.assign_value_to_foreign_key(params, "department", Department, "create")

        period = Period.objects.create(**params)
        return CreatePeriod(period)