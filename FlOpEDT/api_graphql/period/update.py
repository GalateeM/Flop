from graphene_django import DjangoObjectType
import graphene
from django.db import models
from .types import PeriodType
from base.models import Period, Department 
from api_graphql import lib
from graphql_relay import from_global_id

class UpdatePeriod(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(graphene.ID, required = True)
        department =graphene.Argument(graphene.ID)
        starting_week = graphene.Int(graphene.ID, required=True)
        ending_week = graphene.Int(graphene.ID, required = True)


    period = graphene.Field(PeriodType)

    @classmethod
    def mutate(cls, root, info,id, **params):
        id = from_global_id(id)[1]
        period_set = Period.objects.filter(id=id)
        if period_set:
       
            #foreignKey
            lib.assign_value_to_foreign_key(params, "department", Department, "update")

            period_set.update(**params)
            period = period_set.first()
            period.save()
            return UpdatePeriod(period)
        else:
            print('Period with given ID does not exist in the database')

    
    