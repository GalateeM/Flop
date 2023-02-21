from graphene_django import DjangoObjectType
import graphene
from django.db import models
from base.models import Course
from .types import CourseNode

class UpdateCourse(graphene.Mutation):
    class Arguments:
        no = graphene.Int()
        suspens = graphene.Boolean()
    courses = graphene.Field(CourseNode)
    @classmethod
    def mutate(cls, root, info,no, **update_data):
        courses = courses.objects.filter(no=no)
        if courses:
            params = update_data
            courses.update(**{k:v for k, v in params.items() if params[k]})
            return UpdateCourse(courses=courses.first())
        
        else:
            print("Course with the following Id does not exst in database")