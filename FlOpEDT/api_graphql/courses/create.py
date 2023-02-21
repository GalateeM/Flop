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
    
        courses = Course.objects.create(**{k: v for k, v in params.items() if params[k] and k not in ["supp_tutor","groups","module","modulesupp","pay_module"]})
        supp_tutor = TutorType.get_supp_tutor(params["supp_tutor"])
        groups = GenericGroupNode.get_groups(params["groups"])
        module = ModuleNode.get_module(params["modules"])
        modulesupp = ModuleNode.get_modulesupp(params["modulesupp"])
        pay_module = ModuleNode.get_pay_module(params["pay_module"])
        courses.supp_tutor.set(supp_tutor)
        courses.groups.set(groups)
        courses.module.set(module)
        courses.modulesupp.set(modulesupp)
        courses.pay_module.set(pay_module)
        courses.save()
        
        return CreateCourse(courses=courses, supp_tutor = courses.supp_tutor.all(), groups= courses.groups.all(), module = courses.module.all(), modulesupp = courses.modulesupp.all(),pay_module = courses.pay_module.all())

