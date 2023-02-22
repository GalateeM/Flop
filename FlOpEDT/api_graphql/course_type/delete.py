from graphene_django import DjangoObjectType
import graphene
from base.models import CourseType
from .types import CourseTypeNode
from graphql_relay import from_global_id

class DeleteCourseType(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
         
    course_type = graphene.Field(CourseTypeNode)

    @classmethod
    def mutate(cls, root, info, id):
        id = from_global_id(id) [1]
        try:
            course_type = CourseType.objects.get(id=id)
            course_type.delete()
            return DeleteCourseType(course_type)
        
        except CourseType.DoesNotExist:
            print('Course Type with given ID does not exist in the database')