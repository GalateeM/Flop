from graphene_django import DjangoObjectType
import graphene
from django.db import models
from base.models import Week
from .types import WeekType
from api_graphql import lib
from graphql_relay import from_global_id

class UpdateWeek(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
        nb = graphene.Int()
        year = graphene.Int()

    week = graphene.Field(WeekType)

    @classmethod
    def mutate(cls,root,info, id, **params):
        id = from_global_id(id)[1]
        week_set = Week.objects.filter(id=id)
        if week_set:
            week_set.update(**params)
            week = week_set.first()
            week.save()

            return UpdateWeek(week)
        else:
            print('Week with given ID does not exist in the database')