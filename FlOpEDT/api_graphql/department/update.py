import graphene
from base.models import Department
from .types import DepartmentType
from graphql_relay import from_global_id

class UpdateDepartment(graphene.Mutation):
    class arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        abbrev = graphene.String()

    departments = graphene.Field(DepartmentType)

    @classmethod
    def mutate(cls, root, info, id, **params):
        id = from_global_id(id) [1]
        departments_set = Department.objects.filter(id=id)
        if departments_set:
            departments_set.update(**params)
            departments = departments_set.first()
            departments.save()
            
            return UpdateDepartment(departments=departments)

        else:
            print('Department with given ID does not exist in the database')