from graphene_django import DjangoObjectType
import graphene
from django.db import models
from base.models import Course
from .types import CourseNode
from graphql_relay import from_global_id

class DeleteCourse(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    courses = graphene.Field(CourseNode)


    @classmethod
    def mutate(cls,root, info, id):
        id = from_global_id(id) [1]
        courses_set = Course.object.get(id=id)

        if courses_set:
            Courses=courses_set.first()
            Courses.delete()
            return DeleteCourse(Courses)
        else:
            print('Course with the given ID does not exist')
        

        