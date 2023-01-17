import graphene
from people.models import Tutor
from .types import TutorType
from api_graphql.department.types import DepartmentType

class CreateTutor(graphene.Mutation):
    class Arguments:
        #abstractBaseUser
        password = graphene.String(required=True)

        #permissionMixins
        is_superuser = graphene.Boolean()

        #abstractUser
        username = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True) 
        is_staff = graphene.Boolean()
        is_active = graphene.Boolean()

        #user
        is_student = graphene.Boolean()
        is_tutor = graphene.Boolean()
        rights = graphene.Int()
        departments = graphene.List(graphene.ID, required=True)

        #tutor
        status = graphene.String()


    tutor = graphene.Field(TutorType)
    departments = graphene.List(DepartmentType)

    @classmethod
    def mutate(cls, root, info, **params):
        tutor = Tutor.objects.create(**{k: v for k, v in params.items() if params[k] and k != "departments"})
        departments = DepartmentType.get_departments(params["departments"])
        tutor.departments.set(departments)
        tutor.save()
        
        return CreateTutor(tutor=tutor, departments = tutor.departments.all())