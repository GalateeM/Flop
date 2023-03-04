import graphene
from people.models import Tutor
from .types import TutorType
from api_graphql.department.types import DepartmentType
from base.models import Department
from graphql_relay import from_global_id

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
    # manyToManyField
    departments = graphene.List(DepartmentType)
    # #################

    @classmethod
    def mutate(cls, root, info, **params):
        # manyToManyField
        departments_ids = [ from_global_id(id)[1] for id in params["departments"]]
        departments = Department.objects.filter(pk__in = departments_ids)
        del params["departments"]
        # #################
        
        tutor = Tutor.objects.create(**{k: v for k, v in params.items()})
        tutor.departments.add(*departments)
        tutor.save()
        
        return CreateTutor(tutor=tutor, departments = tutor.departments.all())