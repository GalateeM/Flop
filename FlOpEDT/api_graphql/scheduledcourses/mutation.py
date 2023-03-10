from api_graphql.base import BaseMutation
from .create import CreateScheduledCourse
from .update import UpdateScheduledCourse
from .delete import DeleteScheduledCourse

class Mutation(BaseMutation):
    
    """
     This class contains the fields of models that are supposed to be 
     mutated.
     """

    create_scheduled_course= CreateScheduledCourse.Field()
    update_scheduled_course = UpdateScheduledCourse.Field()
    delete_scheduled_course = DeleteScheduledCourse.Field()

