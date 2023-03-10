import graphene
from base.models import  Course, ScheduledCourse, Room, Tutor
from .types import ScheduledCourse  
from people.models import Tutor
from graphql_relay import from_global_id
from api_graphql import lib

class CreateScheduledCourse(graphene.Mutation):
    class Arguments:
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
    def mutate(cls,root,info, **params):

        #foreignkey
        lib.assign_value_to_foreign_key(params,"course", Course, "create")
        lib.assign_value_to_foreign_key(params,"room", Room, "create")
        lib.assign_value_to_foreign_key(params,"tutor", Tutor, "create")
        
        scheduled_courses = ScheduledCourse.objects.create(**params)
        return CreateScheduledCourse(scheduled_courses)


