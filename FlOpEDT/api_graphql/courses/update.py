from graphene_django import DjangoObjectType
import graphene
from django.db import models
from base.models import Course, CourseType, Module, RoomType, Week
from people.models import Tutor
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
from api_graphql import lib

class UpdateCourse(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        type = graphene.Argument(graphene.ID)
        room_type = graphene.Argument(graphene.ID)
        no = graphene.Int()
        tutor = graphene.Argument(graphene.ID)
        supp_tutor = graphene.List(graphene.ID)
        groups = graphene.List(graphene.ID)
        module = graphene.Argument(graphene.ID)
        modulesupp = graphene.Argument(graphene.ID)
        pay_module = graphene.Argument(graphene.ID)
        week = graphene.Argument(graphene.ID)
        suspens = graphene.Boolean()

    courses = graphene.Field(CourseNode)
    supp_tutor = graphene.List(TutorType)
    
    @classmethod
    def mutate(cls, root, info,id, **params):
        id = from_global_id(id)[1]
        courses_set = Course.objects.filter(id=id)
        if courses_set:
            #foreign key
            lib.assign_value_to_foreign_key(params, "type", CourseType, "update")
            lib.assign_value_to_foreign_key(params, "module", Module, "update")
            lib.assign_value_to_foreign_key(params, "room_type", RoomType, "update")
            lib.assign_value_to_foreign_key(params, "tutor", Tutor, "update")
            lib.assign_value_to_foreign_key(params, "modulesupp", Module, "update")
            lib.assign_value_to_foreign_key(params, "pay_module", Module, "update")
            lib.assign_value_to_foreign_key(params, "week", Week, "update")

            #ManyToMany
            supp_tutor_ids =[]
            supp_tutor = None
            if params.get("supp_tutor") != None:
                supp_tutor_ids = [ from_global_id(id)[1] for id in params["supp_tutor"] ]
                supp_tutor = Tutor.objects.filter(id__in = supp_tutor_ids)
                del params["supp_tutor"]

            groups_ids = []
            groups = None
            if params.get("groups") != None:
                groups_ids = [ from_global_id(id)[1] for id in params["groups"] ]
                groups= Tutor.objects.filter(id__in = groups_ids)
                del params["groups"]
       
            courses_set.update(**params)
            courses= courses_set.first()
            if groups != None:
                courses.groups.clear()
                courses.groups.add(*groups)
            if supp_tutor != None:
                courses.supp_tutor.clear()
                courses.supp_tutor.add(*supp_tutor)
            courses.save()

            return UpdateCourse(courses=courses, supp_tutor=courses.supp_tutor.all())
        else:
            print('Course Type with given ID does not exist in the database')