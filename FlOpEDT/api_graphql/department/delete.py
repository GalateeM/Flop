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
        departments_set = Department.objects.filter(id=id)
        if departments_set:
            departments = departments_set.first()
            departments.delete()
            return DeleteDepartment(departments)
        else:
            print('Department with given ID does not exist in the database')