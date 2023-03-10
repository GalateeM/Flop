import graphene
from base.models import  Course, ScheduledCourse, Room
from .types import ScheduledCourseNode
from people.models import Tutor
from graphql_relay import from_global_id
from api_graphql import lib

class DeleteScheduledCourse(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    scheduled_courses = graphene.Field(ScheduledCourseNode)

    @classmethod
    def mutate(cls, root, info,id, **params):
        id = from_global_id(id)[1]
        try:
            scheduled_course = ScheduledCourse.objects.get(id=id)
            scheduled_course.delete()

            return DeleteScheduledCourse(scheduled_course)
        except ScheduledCourse.DoesNotExist:
            print("Scheduled Course with the given Id does not exist in the database")