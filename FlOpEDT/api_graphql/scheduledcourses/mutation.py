from api_graphql.base import BaseMutation
from .create import CreateScheduledCourse
from .update import UpdateScheduledCourse
from .delete import DeleteScheduledCourse

class Mutation(BaseMutation):
    create_scheduled_course = CreateScheduledCourse.Field()
    update_scheduled_course = UpdateScheduledCourse.Field()
    delete_scheduled_course = DeleteScheduledCourse.Field()