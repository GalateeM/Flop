from graphene_django import DjangoObjectType
from base.models import CourseType
import graphene
from .types import CourseTypeNode

class UpdateCourseType(graphene.Mutation):
    class arguments:
        name = graphene.String()
        duration = graphene.Int()
        pay_duration = graphene.Int()
        graded = graphene.Boolean()
    
    CourseType = graphene.Field(CourseTypeNode)

    @classmethod
    def mutate(cls, root, info, name, **update_data):
        courseType = CourseType.objects.filter(name=name)
        if courseType:
            params = update_data
            courseType.update(**{k: v for k, v in params.items() if params[k]})
            return UpdateCourseType(courseType=courseType.first())
        else:
            print('Tutor with given ID does not exist in the database')
