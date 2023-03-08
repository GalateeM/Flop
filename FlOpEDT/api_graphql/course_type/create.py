import graphene
from base.models import CourseType, GroupType, Department
from .types import CourseTypeNode
from api_graphql.group_type.types import GroupTypeNode
from graphql_relay import from_global_id
from api_graphql import lib

class CreateCourseType(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        department = graphene.Argument(graphene.ID)
        duration = graphene.Int()
        pay_duration = graphene.Int()
        group_types = graphene.List(graphene.ID, required=True)
        graded = graphene.Boolean()
    
    course_type = graphene.Field(CourseTypeNode)
    # manyToManyField
    group_types = graphene.List(GroupTypeNode)
    # #################
    
    @classmethod
    def mutate(cls, root, info, **params):
        # foreign keys
        lib.assign_value_to_foreign_key(params, "department", Department, "create")
        
        # manyToManyField
        group_types = lib.get_manyToManyField_values(params, "group_types", GroupType)
        # #################

        course_type = CourseType.objects.create(**params)
        lib.assign_values_to_manyToManyField(course_type, "group_types", group_types)
        course_type.save()
        
        return CreateCourseType(course_type=course_type, group_types = course_type.group_types.all())