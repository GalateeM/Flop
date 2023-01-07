from people.models import Tutor
import graphene
from .types import TutorType
from graphql_relay import from_global_id
from api_graphql.department.types import DepartmentType

class UpdateTutor(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        
        #abstractBaseUser
        password = graphene.String()

        #permissionMixins
        is_superuser = graphene.Boolean()

        #abstractUser
        username = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String() 
        is_staff = graphene.Boolean()
        is_active = graphene.Boolean()

        #user
        is_student = graphene.Boolean()
        is_tutor = graphene.Boolean()
        rights = graphene.Int()
        departments = graphene.List(graphene.ID)

        #tutor
        status = graphene.String()

    tutor = graphene.Field(TutorType)
    departments = graphene.List(DepartmentType)

    @classmethod
    def mutate(cls, root, info, id, **params):
        id = from_global_id(id) [1]
        tutor_set = Tutor.objects.filter(id=id)
        if tutor_set:
            tutor_set.update(**{k: v for k, v in params.items() if params[k] and k != "departments"})
            departments = DepartmentType.get_departments(params.get("departments", []))
            tutor = tutor_set.first()
            if len(departments) > 0:
                tutor.departments.set(departments)
            tutor.save()

            return UpdateTutor(tutor=tutor,departments = tutor.departments.all())
        
        else:
            print('Tutor with given ID does not exist in the database')