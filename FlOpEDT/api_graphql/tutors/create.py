import graphene

from people.models import Tutor
from base.models import Department

from api_graphql import lib
from .types import TutorType
from api_graphql.department.types import DepartmentType


class CreateTutor(graphene.Mutation):
    class Arguments:
        password = graphene.String(required=True)
        is_superuser = graphene.Boolean()
        username = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True) 
        is_staff = graphene.Boolean()
        is_active = graphene.Boolean()
        is_student = graphene.Boolean()
        is_tutor = graphene.Boolean()
        rights = graphene.Int()
        departments = graphene.List(graphene.ID, required=True)
        status = graphene.String()

    tutor = graphene.Field(TutorType)
    departments = graphene.List(DepartmentType)

    @classmethod
    def mutate(cls, root, info, **params):
        departments = lib.get_manyToManyField_values(params, "departments", Department)
        
        tutor = Tutor.objects.create(**params)
        lib.assign_values_to_manyToManyField(tutor, "departments", departments)
        tutor.save()
        return CreateTutor(tutor=tutor, departments = tutor.departments.all())