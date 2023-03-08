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
    # manyToManyField
    group_types = graphene.List(GroupTypeNode)
    # #################
    
    @classmethod
    def mutate(cls, root, info, **params):
        # foreign keys
        department = None
        if params.get("department") != None:
            id = from_global_id(params["department"])[1]
            department = Department.objects.get(id=id)
            del params["department"]
        
        # manyToManyField
        group_types_ids = [ from_global_id(id)[1] for id in params["group_types"]]
        group_types = GroupType.objects.filter(pk__in = group_types_ids)
        del params["group_types"]
        # #################

        course_type = CourseType.objects.create(**params)
        course_type.department = department
        course_type.save()
        course_type.group_types.add(*group_types)
        course_type.save()
        
        return CreateCourseType(course_type=course_type, group_types = course_type.group_types.all())

""" mutation {
  createCourseType (
    name : "CourseType1"
    department : "RGVwYXJ0bWVudFR5cGU6MzE="
    groupTypes : ["R3JvdXBUeXBlTm9kZTo5MA==", "R3JvdXBUeXBlTm9kZTo5NA=="]
    graded : true
  ) {
  	courseType {
      id
      name
      department {
        id
        abbrev
        name
      }
    }
    groupTypes {
      name
      department
    }
  }
} """

""" mutation {
  updateCourseType (
    id : "Q291cnNlVHlwZU5vZGU6MTc0"
    name : "CourseType7"
    department : "R3JvdXBUeXBlTm9kZTo5Mg=="
    groupTypes : ["RGVwYXJ0bWVudFR5cGU6MzA="]
    graded : true
  ) {
  	courseType {
      id
      name
      department {
        id
        abbrev
        name
      }
    }
    groupTypes {
      name
      department
    }
  }
} """

# "R3JvdXBUeXBlTm9kZTo5Mg==" td parcours
# "RGVwYXJ0bWVudFR5cGU6MzA=" genie industr et maintenance