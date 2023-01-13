from graphene_django import DjangoObjectType
import graphene
from base.models import CourseType
from .types import CourseTypeNode

class DeleteCourseType(graphene.Mutation):
    class arguments:
        name = graphene.String()
    
    courseType = graphene.Field(CourseTypeNode)

    @classmethod
    def mutate(cls,root,info,name):
        courseType = CourseType.objects.get(name=name)
        courseType.delete()
        return DeleteCourseType