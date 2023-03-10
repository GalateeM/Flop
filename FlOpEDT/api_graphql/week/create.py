from graphene_django import DjangoObjectType
import graphene
from django.db import models
from base.models import Week
from .types import WeekType
from api_graphql import lib

class CreateWeek(graphene.Mutation):
    class Arguments:
        nb = graphene.Int(required = True)
        year = graphene.Int(required = True)

    week = graphene.Field(WeekType)

    @classmethod
    def mutate(cls,root,info, **params):
        week = Week.objects.create(**params)
        return Week(week)