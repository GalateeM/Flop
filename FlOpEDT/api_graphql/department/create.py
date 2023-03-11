import graphene

from base.models import Department

from .types import DepartmentType


class CreateDepartment(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        abbrev = graphene.String(required=True)

    department = graphene.Field(DepartmentType)

    @classmethod
    def mutate(cls, root, info, **params):
        department = Department.objects.create(**params)
        return CreateDepartment(department=department)