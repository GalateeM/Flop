from graphene_django import DjangoObjectType
import graphene
from django.db import models
from base.models import CourseType, GroupType
from api_graphql.department.types import DepartmentType
from .types import CourseTypeNode

class CreateCourseType(graphene.Mutation):
    class arguments:
        name = graphene.String(required=True)
        duration = graphene.Int(required=True)
        pay_duration = graphene.Int()
        graded = graphene.Boolean(required=True)
        group_types = graphene.List(GroupType)
        department = graphene.Field(DepartmentType)
    
    courseTypes = graphene.Field(CourseTypeNode)

    @classmethod
    def mutate(cls, root, info, **user_data):
        courseType = CourseType(
            name=user_data.get('name'),
            duration=user_data.get('duration'),
            pay_duration=user_data.get('pay_duration'),
            graded=user_data.get('graded'),
        )

        return CreateCourseType(courseType=courseType)

