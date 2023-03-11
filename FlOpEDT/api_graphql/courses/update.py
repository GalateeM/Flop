import graphene
from graphql_relay import from_global_id

from base.models import Course, CourseType, Module, RoomType, Week, GenericGroup
from people.models import Tutor

from api_graphql import lib
from .types import CourseNode
from api_graphql.tutors.types import TutorType


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
    def mutate(cls, root, info, id, **params):
        id = from_global_id(id)[1]
        courses_set = Course.objects.filter(id=id)
        if courses_set:
            lib.assign_value_to_foreign_key(params, "type", CourseType, "update")
            lib.assign_value_to_foreign_key(params, "module", Module, "update")
            lib.assign_value_to_foreign_key(params, "room_type", RoomType, "update")
            lib.assign_value_to_foreign_key(params, "tutor", Tutor, "update")
            lib.assign_value_to_foreign_key(params, "modulesupp", Module, "update")
            lib.assign_value_to_foreign_key(params, "pay_module", Module, "update")
            lib.assign_value_to_foreign_key(params, "week", Week, "update")

            supp_tutor = lib.get_manyToManyField_values(params, "supp_tutor", Tutor)
            groups = lib.get_manyToManyField_values(params, "groups", GenericGroup)
            
            courses_set.update(**params)
            courses = courses_set.first()
            lib.assign_values_to_manyToManyField(courses, "supp_tutor", supp_tutor)
            lib.assign_values_to_manyToManyField(courses, "groups", groups)
            courses.save()

            return UpdateCourse(courses=courses, supp_tutor=courses.supp_tutor.all())
        else:
            print('Course Type with given ID does not exist in the database')