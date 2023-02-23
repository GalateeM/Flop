from graphene_django import DjangoObjectType
import graphene
from django.db import models
from base.models import Course, CourseType
from .types import CourseNode
from api_graphql.course_type.types import CourseTypeNode 
from api_graphql.room_type.types import RoomTypeNode
from api_graphql.tutors.types import TutorType
from api_graphql.generic_group.types import GenericGroupNode
from api_graphql.module.types import ModuleNode
from api_graphql.week.types import WeekType
from graphql_relay import from_global_id

class CreateCourse(graphene.Mutation):
    class arguments:
        type = graphene.Argument(graphene.ID, required=True)
        room_type = graphene.Argument(graphene.ID)
        no = graphene.Int()
        tutor = graphene.Argument(graphene.ID)
        supp_tutor = graphene.List(graphene.ID, required=True)
        groups = graphene.List(graphene.ID, required=True)
        module = graphene.Argument(graphene.ID, required=True)
        modulesupp = graphene.Argument(graphene.ID)
        pay_module = graphene.Argument(graphene.ID)
        week = graphene.Argument(graphene.ID)
        suspens = graphene.Boolean()


    
    courses = graphene.Field(CourseNode)

    @classmethod
    def mutate(cls,root,info, **params):
        # foreignKey
        id_type = from_global_id(params["type"])[1]
        type = CourseType.objects.get(id=id_type)
        del params["type"]

        id_supp_tutor = from_global_id(params["supp_tutor"])[1]
        supp_tutor = TutorType.objects.get(id=id_supp_tutor)
        del params["supp_tutor"]

        id_groups = from_global_id(params["groups"])[1]
        groups = GenericGroupNode.objects.get(id=id_groups)
        del params["groups"]

        id_module = from_global_id(params["module"])[1]
        module = ModuleNode.objects.get(id=id_module)
        del params["module"]

        """ Si required=False , rajouter ça avant
        type = None
        if params.get("type") != None:
        """
        
        # manyToManyField
        supp_tutor = TutorType.get_supp_tutor(params["supp_tutor"])
        del params["supp_tutor"]

        groups = GenericGroupNode.get_groups(params["groups"])
        del params
        module = ModuleNode.get_module(params["modules"])
        del params[""]
        modulesupp = ModuleNode.get_modulesupp(params["modulesupp"])
        del params["modulesupp"]
        pay_module = ModuleNode.get_pay_module(params["pay_module"])
        courses.groups.set(groups)
        courses.module.set(module)
        courses.modulesupp.set(modulesupp)
        courses.pay_module.set(pay_module)
        courses = Course.objects.create(**{k: v for k, v in params.items()})
        courses.type = type # foreignKey
        courses.supp_tutor.set(supp_tutor) # manyToManyField
        courses.save()
        
        return CreateCourse(courses=courses, supp_tutor = courses.supp_tutor.all(), groups= courses.groups.all(), module = courses.module.all(), modulesupp = courses.modulesupp.all(),pay_module = courses.pay_module.all())

