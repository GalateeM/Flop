import graphene
from base.models import Department
from .types import DepartmentType
from graphql_relay import from_global_id

class DeleteDepartment(graphene.Mutation):
    class arguments:
        id = graphene.ID(required= True)

    departments = graphene.Field(DepartmentType)

    @classmethod
    def mutate(cls, root, info, id):
        id = from_global_id(id) [1]
        try:
            departments = Department.objects.get(id=id)
            departments.delete()
            return DeleteDepartment(departments)
        except Department.DoesNotExist:
            print('Department with given ID does not exist in the database')