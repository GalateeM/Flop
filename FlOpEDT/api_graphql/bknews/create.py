from graphene_django import DjangoObjectType
import graphene
from django.db import models
from displayweb.models import BreakingNews
from .types import BknewsType
from api_graphql.department.types import DepartmentType

class CreateBknews(graphene.Mutation):
    class Arguments:
        week = graphene.Int()
        year = graphene.Int()
        txt = graphene.String()
        department = graphene.Field(DepartmentType)
        x_beg = graphene.Float()
        x_end = graphene.Float()
        y = graphene.Int()
        is_linked = graphene.Srting()
        fill_color = graphene.String()
        strk_color = graphene.String()
        # argument facultatif

    bknews = graphene.Field(BknewsType)

    @classmethod
    def mutate(cls, root, info, **user_data):
        bknews = BreakingNews(
            week=user_data.get('week'),
            year=user_data.get('year'),
            txt=user_data.get('txt'),
            department=user_data.get('department'),
            x_beg = user_data.get('x_beg'),
            x_end = user_data.get('x_end'),
            y = user_data.get('y'),
            is_linked = user_data.get('is_linked'),
            fill_color =user_data.get('fill_color'),
            strk_color =user_data.get('strk_color')
        )
        
        bknews.save()
        return CreateBknews(bknews=bknews)