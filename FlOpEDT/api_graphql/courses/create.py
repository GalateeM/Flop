from graphene_django import DjangoObjectType
import graphene
from django.db import models
from base.models import Course
from .types import CourseNode
from api_graphql.course_type.types import CourseTypeNode 
from api_graphql.room_type.types import RoomTypeNode
from api_graphql.tutors.types import TutorType
from api_graphql.generic_group.types import GenericGroupNode
from api_graphql.module.types import ModuleNode
from api_graphql.week.types import WeekType

class CreateCourse(graphene.Mutation):
    class arguments:
        no = graphene.Int()
        suspens = graphene.Boolean()

        type = graphene.Field(CourseTypeNode)
        room_type = graphene.Field(RoomTypeNode)
        tutor = graphene.Field(TutorType)
        week = graphene.Field(WeekType)

        supp_tutor = graphene.List(TutorType)
        groups = graphene.List(GenericGroupNode)
        module = graphene.List(ModuleNode)
        modulesupp = graphene.List(ModuleNode)
        pay_module = graphene.List(ModuleNode)
    
    courses = graphene.Field(CourseNode)

    @classmethod
    def mutate(cls,root,info, **user_data):
        courses = Course(
            no = user_data.get('no'),

        )
