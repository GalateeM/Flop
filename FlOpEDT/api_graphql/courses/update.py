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
from people.models import Tutor
from base.models import GenericGroup
from graphql_relay import from_global_id

class UpdateCourse(graphene.Mutation):
    class Arguments:
        no = graphene.Int()
        suspens = graphene.Boolean()

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
    def mutate(cls, root, info,id, **params):
        id = from_global_id(id)[1]
        courses_set = courses.objects.filter(id=id)
        if courses_set:
            #foreign key
            if params.get("RoomType")!=None:
                params["room_type"]= from_global_id(params["room_type"])[1]
            if params.get("Tutor")!=None:
                params["tutor"]= from_global_id(params["tutor"])[1]
            if params.get("Module")!=None:
                params["modulesupp"]= from_global_id(params["modulesupp"])[1]
            if params.get("Module")!=None:
                params["pay_module"]= from_global_id(params["pay_module"])[1]
            if params.get("Week")!=None:
                params["week"]= from_global_id(params["week"])[1]

            #ManyToMany


            supp_tutor_ids =[]
            supp_tutor = None
            if params.get("supp_tutor") != None:
                supp_tutor_ids = [ from_global_id(id)[1] for id in params["supp_tutor"] ]
                supp_tutor = Tutor.objects.filter(id__in = supp_tutor_ids)
                del params["supp_tutor"]



            groups_ids =[]
            groups = None
            if params.get("groups") != None:
                groups_ids = [ from_global_id(id)[1] for id in params["groups"] ]
                groups= Tutor.objects.filter(id__in = groups_ids)
                del params["groups"]
       

            
           
        
            courses_set.update(**{k: v for k, v in params.items()})
            courses= courses_set.first()
            if groups != None:
                courses.groups.add(*groups)
            if supp_tutor != None:
                courses.supp_tutor.add(*supp_tutor)
            courses.save()

            return UpdateCourse(courses=courses, groups= courses.groups.all(), supp_tutor=courses.supp_tutor.all())
        else:
            print('Course Type with given ID does not exist in the database')