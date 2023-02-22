from graphene_django import DjangoObjectType
from base.models import CourseType
import graphene
from .types import CourseTypeNode
from api_graphql.group_type.types import GroupTypeNode
from graphql_relay import from_global_id

class UpdateCourseType(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        department = graphene.Argument(graphene.ID)
        duration = graphene.Int()
        pay_duration = graphene.Int()
        group_types = graphene.List(graphene.ID)
        graded = graphene.Boolean()
    
    course_type = graphene.Field(CourseTypeNode)
    # manyToManyField
    group_types = graphene.List(GroupTypeNode)
    # #################

    @classmethod
    def mutate(cls, root, info, id, **params):
        id = from_global_id(id) [1]
        course_type_set = CourseType.objects.filter(id=id)
        if course_type_set:
            # foreign keys
            if params.get("department") != None:
                params["department"] = from_global_id(params["department"])[1]
            # ##############

            # manyToManyField
            group_types_ids = []
            if params.get("departments") != None:
                group_types_ids = [ from_global_id(id)[1] for id in params["group_types"]]
                del params["group_types"]
            # ###################
        
            course_type_set.update(**{k: v for k, v in params.items()})
            course_type = course_type_set.first()
            if len(group_types_ids) > 0:
                print("blablablabla7777777")
                course_type.group_types.set(group_types_ids)
            course_type.save()

            return UpdateCourseType(course_type=course_type, group_types = course_type.group_types.all())
        else:
            print('Course Type with given ID does not exist in the database')