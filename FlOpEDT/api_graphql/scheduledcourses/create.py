import graphene

from base.models import  Course, ScheduledCourse, Room
from people.models import Tutor

from api_graphql import lib
from .types import ScheduledCourseNode


class CreateScheduledCourse(graphene.Mutation):
    class Arguments:
        course = graphene.Argument(graphene.ID, required = True)
        day = graphene.String()
        start_time = graphene.Int()
        room = graphene.Argument(graphene.ID)
        no = graphene.Int()
        noprec = graphene.Boolean()
        work_copy = graphene.Int()
        tutor = graphene.Argument(graphene.ID)

    scheduled_courses = graphene.Field(ScheduledCourseNode)

    @classmethod
    def mutate(cls,root,info, **params):
        lib.assign_value_to_foreign_key(params,"course", Course, "create")
        lib.assign_value_to_foreign_key(params,"room", Room, "create")
        lib.assign_value_to_foreign_key(params,"tutor", Tutor, "create")
        
        scheduled_courses = ScheduledCourse.objects.create(**params)
        return CreateScheduledCourse(scheduled_courses)