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
        """ id_type = from_global_id(params["type"])[1]
        type = CourseType.objects.get(id=id_type)
        del params["type"]

        id_module = from_global_id(params["module"])[1]
        module = Module.objects.get(id=id_module)
        del params["module"]

        room_type = None
        if params.get("room_type")!=None:
            id_room_type = from_global_id(params["room_type"])[1]
            room_type = RoomType.objects.get(id=id_room_type)
            del params["room_type"]

        tutor = None
        if params.get("tutor")!=None:
            id_tutor= from_global_id(params["tutor"])[1]
            tutor = Tutor.objects.get(id=id_tutor)
            del params["tutor"]

        modulesupp = None
        if params.get("modulesupp")!=None:
            id_modulesupp= from_global_id(params["modulesupp"])[1]
            modulesupp= Module.objects.get(id=id_modulesupp)
            del params["modulesupp"]


        pay_module = None
        if params.get("pay_module")!=None:
            id_pay_module= from_global_id(params["pay_module"])[1]
            pay_module= Module.objects.get(id=id_pay_module)
            del params["pay_module"]

        week= None
        if params.get("week")!=None:
            id_week= from_global_id(params["week"])[1]
            week= Week.objects.get(id=id_week)
            del params["week"] """
        
        lib.assign_value_to_foreign_key(params, "type", CourseType, "create")
        lib.assign_value_to_foreign_key(params, "module", Module, "create")
        lib.assign_value_to_foreign_key(params, "room_type", RoomType, "create")
        lib.assign_value_to_foreign_key(params, "tutor", Tutor, "create")
        lib.assign_value_to_foreign_key(params, "modulesupp", Module, "create")
        lib.assign_value_to_foreign_key(params, "pay_module", Module, "create")
        lib.assign_value_to_foreign_key(params, "week", Week, "create")
        # manyToManyField
        """ supp_tutor_ids = [ from_global_id(id)[1] for id in params["supp_tutor"] ]
        supp_tutor = Tutor.objects.filter(id__in=supp_tutor_ids)
        del params["supp_tutor"]

        groups_ids = [ from_global_id(id)[1] for id in params["groups"]]
        groups = GenericGroup.objects.filter(id__in = groups_ids)
        del params["groups"] """
        supp_tutor = lib.get_manyToManyField_values(params, "supp_tutor", Tutor)
        groups = lib.get_manyToManyField_values(params, "groups", GenericGroup)
        
        """ courses = None
        if len(params) > 0:
            courses = Course.objects.create(**{k: v for k, v in params.items()})
        else:
            courses = Course.objects.create(module=module, type=type)
        
        courses.type = type # foreignKey
        courses.room_type = room_type
        courses.tutor = tutor
        courses.module = module
        courses.modulesupp = modulesupp
        courses.pay_module = pay_module
        courses.week = week
        courses.save() """
        courses = Course.objects.create(**params)
        courses.save()

        """ courses.supp_tutor.add(*supp_tutor) # manyToManyField
        courses.save()
        courses.groups.add(*groups)
        courses.save() """
        lib.assign_values_to_manyToManyField(courses, "supp_tutor", supp_tutor)
        lib.assign_values_to_manyToManyField(courses, "groups", groups)
        
        return CreateCourse(courses=courses, supp_tutor = courses.supp_tutor.all())

