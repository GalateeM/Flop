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
        try:
            courses= Course.objects.get(id=id)
            courses.delete()
            return DeleteCourse(courses)
        
        except Course.DoesNotExist:
            print('Course Type with given ID does not exist in the database')