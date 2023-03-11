import graphene

from base.models import Course, CourseType, Module, Week, RoomType
from api_graphql.tutors.types import TutorType
from people.models import Tutor
from base.models import GenericGroup

from api_graphql import lib
from .types import CourseNode


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
   

    @classmethod
    def mutate(cls,root,info, **params):
        lib.assign_value_to_foreign_key(params, "type", CourseType, "create")
        lib.assign_value_to_foreign_key(params, "module", Module, "create")
        lib.assign_value_to_foreign_key(params, "room_type", RoomType, "create")
        lib.assign_value_to_foreign_key(params, "tutor", Tutor, "create")
        lib.assign_value_to_foreign_key(params, "modulesupp", Module, "create")
        lib.assign_value_to_foreign_key(params, "pay_module", Module, "create")
        lib.assign_value_to_foreign_key(params, "week", Week, "create")
        
        supp_tutor = lib.get_manyToManyField_values(params, "supp_tutor", Tutor)
        groups = lib.get_manyToManyField_values(params, "groups", GenericGroup)
        
        courses = Course.objects.create(**params)
        lib.assign_values_to_manyToManyField(courses, "supp_tutor", supp_tutor)
        lib.assign_values_to_manyToManyField(courses, "groups", groups)
        courses.save()
        
        return CreateCourse(courses=courses, supp_tutor = courses.supp_tutor.all())