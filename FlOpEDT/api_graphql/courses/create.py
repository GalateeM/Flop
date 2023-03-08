from graphene_django import DjangoObjectType
import graphene
from django.db import models
from base.models import Course, CourseType, Module, Week, RoomType
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
    supp_tutor = graphene.List(TutorType)
    # groups non rajouté car le query de GenericGroup contient un filtre obligatoire sur dept
   

    @classmethod
    def mutate(cls,root,info, **params):
        # foreignKey  
        lib.assign_value_to_foreign_key(params, "type", CourseType, "create")
        lib.assign_value_to_foreign_key(params, "module", Module, "create")
        lib.assign_value_to_foreign_key(params, "room_type", RoomType, "create")
        lib.assign_value_to_foreign_key(params, "tutor", Tutor, "create")
        lib.assign_value_to_foreign_key(params, "modulesupp", Module, "create")
        lib.assign_value_to_foreign_key(params, "pay_module", Module, "create")
        lib.assign_value_to_foreign_key(params, "week", Week, "create")
        
        # manyToManyField
        supp_tutor = lib.get_manyToManyField_values(params, "supp_tutor", Tutor)
        groups = lib.get_manyToManyField_values(params, "groups", GenericGroup)
        
        courses = Course.objects.create(**params)
        lib.assign_values_to_manyToManyField(courses, "supp_tutor", supp_tutor)
        lib.assign_values_to_manyToManyField(courses, "groups", groups)
        courses.save()
        
        return CreateCourse(courses=courses, supp_tutor = courses.supp_tutor.all())