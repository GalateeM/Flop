from api_graphql.base import BaseMutation
from .create import CreateDepartment
from .update import UpdateDepartment
from .delete import DeleteDepartment

class Mutation(BaseMutation):

    create_departments = CreateDepartment.Field()
    update_departments = UpdateDepartment.Field()
    delete_departments = DeleteDepartment.Field()