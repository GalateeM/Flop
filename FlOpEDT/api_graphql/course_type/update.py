import graphene
from graphql_relay import from_global_id

from base.models import CourseType, GroupType, Department

from api_graphql import lib
from .types import CourseTypeNode
from api_graphql.group_type.types import GroupTypeNode


class UpdateCourseType(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        department = graphene.Argument(graphene.ID)
        duration = graphene.Int()
        pay_duration = graphene.Int()
        group_types = graphene.List(graphene.ID)
        graded = graphene.Boolean()
    
    course_type = graphene.Field(CourseTypeNode)
    group_types = graphene.List(GroupTypeNode)

    @classmethod
    def mutate(cls, root, info, id, **params):
        id = from_global_id(id) [1]
        course_type_set = CourseType.objects.filter(id=id)
        if course_type_set:
            lib.assign_value_to_foreign_key(params, "department", Department, "update")

            group_types = lib.get_manyToManyField_values(params, "group_types", GroupType)
        
            course_type_set.update(**params)
            course_type = course_type_set.first()
            lib.assign_values_to_manyToManyField(course_type, "group_types", group_types)
            course_type.save()

            return UpdateCourseType(course_type=course_type, group_types = course_type.group_types.all())
        else:
            print('Course Type with given ID does not exist in the database')