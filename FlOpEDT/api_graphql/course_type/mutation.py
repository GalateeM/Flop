from api_graphql.base import BaseMutation
from .create import CreateCourseType
from .update import UpdateCourseType
from .delete import DeleteCourseType

class Mutation(BaseMutation):
    create_courseType = CreateCourseType.Field()
    update_courseType = UpdateCourseType.Field()
    delete_courseType = DeleteCourseType.Field()