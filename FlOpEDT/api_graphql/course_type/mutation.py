from api_graphql.base import BaseMutation
from .create import CreateCourseType
from .update import UpdateCourseType
from .delete import DeleteCourseType

class Mutation(BaseMutation):
    create_course_type = CreateCourseType.Field()
    update_course_type = UpdateCourseType.Field()
    delete_course_type = DeleteCourseType.Field()