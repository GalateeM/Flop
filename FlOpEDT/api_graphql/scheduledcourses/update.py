import graphene
from base.models import  Course, ScheduledCourse, Room
from people.models import Tutor
from .types import ScheduledCourse  
from people.models import Tutor
from graphql_relay import from_global_id
from api_graphql import lib

class UpdateScheduledCourse(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        course = graphene.Argument(graphene.ID)
        day = graphene.String()
        start_time = graphene.Int()
        room = graphene.Argument(graphene.ID)
        no = graphene.Int()
        noprec = graphene.Boolean()
        work_copy = graphene.Int()
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
            print("Scheduled Course with the given does not exist in the database")
