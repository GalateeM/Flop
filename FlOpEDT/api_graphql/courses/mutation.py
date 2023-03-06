from api_graphql.base import BaseMutation
from .create import CreateCourse
from .update import UpdateCourse
from .delete import DeleteCourse

class Mutation(BaseMutation):
    """
    This class contains the fields of models that are supposed to be 
    mutated.
    """
    create_course = CreateCourse.Field()
    # update_course = UpdateCourse.Field()
    delete_course = DeleteCourse.Field()