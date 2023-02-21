import graphene
from base.models import Department
from .types import DepartmentType

class CreateDepartment(graphene.Mutation):
    class arguments:
        #id = graphene.ID()
        name = graphene.String(required=True)
        abbrev = graphene.String(required=True)

    departments = graphene.Field(DepartmentType)

    @classmethod
    def mutate(cls, root, info, **params):

        departments = Department.objects.create(**params)
        departments.save()

        return CreateDepartment(departments=departments)
