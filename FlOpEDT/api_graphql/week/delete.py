from graphene_django import DjangoObjectType
import graphene
from django.db import models
from base.models import Week
from .types import WeekType
from api_graphql import lib
from graphql_relay import from_global_id

class DeleteWeek(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    
    week = graphene.Field(WeekType)

    @classmethod
    def mutate(cls,root, info, id):
        id = from_global_id(id) [1]
        try:
            week = Week.objects.get(id=id)
            week.delete()
            return DeleteWeek(week)
        
        except Week.DoesNotExist:
            print('Week with given ID does not exist in the database')