from api_graphql.base import BaseMutation
from .create import CreateDepartment
from .update import UpdateDepartment
from .delete import DeleteDepartment

class Mutation(BaseMutation):
    create_department = CreateDepartment.Field()
    update_department = UpdateDepartment.Field()
    delete_department = DeleteDepartment.Field()