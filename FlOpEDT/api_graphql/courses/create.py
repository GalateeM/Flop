from graphene_django import DjangoObjectType
import graphene
from django.db import models
from base.models import Course, CourseType, Module, Week
from .types import CourseNode
from api_graphql.course_type.types import CourseTypeNode 
from api_graphql.room_type.types import RoomTypeNode
from api_graphql.tutors.types import TutorType
from api_graphql.generic_group.types import GenericGroupNode
from api_graphql.module.types import ModuleNode
from api_graphql.week.types import WeekType
from people.models import Tutor
from base.models import GenericGroup
from graphql_relay import from_global_id

class CreateCourse(graphene.Mutation):
    class Arguments:
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

        id_module = from_global_id(params["module"])[1]
        module = Module.objects.get(id=id_module)
        del params["module"]

        RoomType = None
        if params.get("RoomType")!=None:
            id_room_type = from_global_id(params["room_type"])[1]
            room_type = RoomType.objects.get(id=id_room_type)
            del params["room_type"]


        Tutor = None
        if params.get("Tutor")!=None:
            id_tutor= from_global_id(params["tutor"])[1]
            tutor = Tutor.objects.get(id=id_tutor)
            del params["tutor"]

        modulesupp = None
        if params.get("Module")!=None:
            id_modulesupp= from_global_id(params["modulesupp"])[1]
            modulesupp= Module.objects.get(id=id_modulesupp)
            del params["modulesupp"]


        pay_module = None
        if params.get("Module")!=None:
            id_pay_module= from_global_id(params["pay_module"])[1]
            pay_module= Module.objects.get(id=id_pay_module)
            del params["pay_module"]

        week= None
        if params.get("Week")!=None:
            id_week= from_global_id(params["week"])[1]
            week= Week.objects.get(id=id_week)
            del params["week"]

        

        """ Si required=False , rajouter ça avant
        type = None
        if params.get("type") != None:
        """
        
        # manyToManyField
        supp_tutor_ids = [ from_global_id(id)[1] for id in params["supp_tutor"] ]
        supp_tutor = Tutor.objects.filter(id__in=supp_tutor_ids)
        del params["supp_tutor"]

        groups_ids = [ from_global_id(id)[1] for id in params["groups"]]
        groups = GenericGroup.objects.filter(id_in = groups_ids)
        del params["groups"]
        
        

        courses = Course.objects.create(**{k: v for k, v in params.items()})
        courses.type = type # foreignKey
        courses.room_type = room_type
        courses.tutor = tutor
        courses.module = module
        courses.modulesupp = modulesupp
        courses.pay_module = pay_module
        courses.week = week
        courses.save()
        
        courses.supp_tutor.add(*supp_tutor) # manyToManyField
        courses.groups.add(*groups)
        courses.save()
        
        return CreateCourse(courses=courses, supp_tutor = courses.supp_tutor.all(), groups= courses.groups.all())

