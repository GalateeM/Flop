import graphene
from base.models import  Course, ScheduledCourse, Room, Tutor
from .types import ScheduledCourse  
from people.models import Tutor
from graphql_relay import from_global_id
from api_graphql import lib

class UpdateScheduledCourse(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        course = graphene.Argument(graphene.ID, required = True)
        day = graphene.String(graphene.ID)
        # in minutes from 12AM
        start_time = graphene.Int(graphene.ID)
        room = graphene.Argument(graphene.ID)
        no = graphene.Int(graphene.ID)
        noprec = graphene.Boolean(graphene.ID)
        work_copy = graphene.Int(graphene.ID)
        tutor = graphene.Argument(graphene.ID)

    scheduled_courses = graphene.Field(ScheduledCourse)

    @classmethod
    def mutate(cls, root, info,id, **params):
        id = from_global_id(id)[1]
        scheduled_course_set = ScheduledCourse.objects.filter(id=id)

        if scheduled_course_set:

            #foreignkey

            lib.assign_value_to_foreign_key(params, "room", Room, "update")
            lib.assign_value_to_foreign_key(params, "tutor", Tutor, "update")
            lib.assign_value_to_foreign_key(params, "course", Course, "update")

            scheduled_course_set.update(**params)
            scheduled_course = scheduled_course_set.first()
            scheduled_course.save()

            return UpdateScheduledCourse(scheduled_course)
        else:
            print("ScheduledCourse with the given does not exist in the database")
