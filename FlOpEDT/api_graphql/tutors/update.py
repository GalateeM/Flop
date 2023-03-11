import graphene
from graphql_relay import from_global_id

from people.models import Tutor
from base.models import Department

from api_graphql import lib
from .types import TutorType
from api_graphql.department.types import DepartmentType


class UpdateTutor(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        password = graphene.String()
        is_superuser = graphene.Boolean()
        username = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String() 
        is_staff = graphene.Boolean()
        is_active = graphene.Boolean()
        is_student = graphene.Boolean()
        is_tutor = graphene.Boolean()
        rights = graphene.Int()
        departments = graphene.List(graphene.ID)
        status = graphene.String()

    tutor = graphene.Field(TutorType)
    departments = graphene.List(DepartmentType)

    @classmethod
    def mutate(cls, root, info, id, **params):
        id = from_global_id(id) [1]
        tutor_set = Tutor.objects.filter(id=id)
        if tutor_set:
            departments = lib.get_manyToManyField_values(params, "departments", Department)
            
            tutor_set.update(**params)
            tutor = tutor_set.first()
            lib.assign_values_to_manyToManyField(tutor, "departments", departments)
            tutor.save()

            return UpdateTutor(tutor=tutor,departments = tutor.departments.all())
        
        else:
            print('Tutor with given ID does not exist in the database')