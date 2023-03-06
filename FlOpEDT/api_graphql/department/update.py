import graphene
from base.models import Department
from .types import DepartmentType
from graphql_relay import from_global_id

class UpdateDepartment(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        abbrev = graphene.String()

    department = graphene.Field(DepartmentType)

    @classmethod
    def mutate(cls, root, info, id, **params):
        id = from_global_id(id) [1]
        department_set = Department.objects.filter(id=id)
        if department_set:
            department_set.update(**params)
            department = department_set.first()
            department.save()
            
            return UpdateDepartment(department=department)

        else:
            print('Department with given ID does not exist in the database')