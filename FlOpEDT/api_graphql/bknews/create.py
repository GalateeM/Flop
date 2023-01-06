from graphene_django import DjangoObjectType
import graphene
from django.db import models
from displayweb.models import BreakingNews
from .types import BknewsType

class CreateBknews(graphene.Mutation):
    class Arguments:
        week = graphene.Int()
        year = graphene.Int()
        txt = graphene.String()
        department = graphene.ID()
        # argument facultatif

    bknews = graphene.Field(BknewsType)

    @classmethod
    def mutate(cls, root, info, **user_data):
        bknews = BreakingNews(
            week=user_data.get('week'),
            year=user_data.get('year'),
            txt=user_data.get('txt'),
            department=user_data.get('department')
        )
        
        bknews.save()
        return CreateBknews(bknews=bknews)