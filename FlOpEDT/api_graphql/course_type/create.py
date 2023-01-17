import graphene
from base.models import CourseType, GroupType, Department
from .types import CourseTypeNode
from api_graphql.group_type.types import GroupTypeNode
from graphql_relay import from_global_id

class CreateCourseType(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        department = graphene.Argument(graphene.ID)
        duration = graphene.Int()
        pay_duration = graphene.Int()
        group_types = graphene.List(graphene.ID, required=True)
        graded = graphene.Boolean()
    
    course_type = graphene.Field(CourseTypeNode)
    #group_types = graphene.List(GroupType)
    

    @classmethod
    def mutate(cls, root, info, **params):
        department = None
        if params.get("department") != None:
            id = from_global_id(params["department"])[1]
            department = Department.objects.get(id=id)
            del params["department"]

        course_type = CourseType.objects.create(**{k: v for k, v in params.items() if params[k] and k != "group_types"})
        group_types = GroupTypeNode.get_group_types(params["group_types"])
        course_type.group_types.set(group_types)
        course_type.department = department
        course_type.save()
        
        return CreateCourseType(course_type=course_type)
        """ return CreateCourseType(course_type=course_type, group_types=group_types) """