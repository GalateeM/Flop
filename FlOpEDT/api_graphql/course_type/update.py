from graphene_django import DjangoObjectType
from base.models import CourseType, GroupType
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
            groupe_types = None
            if params.get("group_types") != None:
                group_types_ids = [ from_global_id(id)[1] for id in params["group_types"] ]
                groupe_types = GroupType.objects.filter(id__in = group_types_ids)
                del params["group_types"]
            # ###################
        
            course_type_set.update(**params)
            course_type = course_type_set.first()
            if groupe_types != None:
                course_type.group_types.clear()
                course_type.group_types.add(*groupe_types)
            course_type.save()

            return UpdateCourseType(course_type=course_type, group_types = course_type.group_types.all())
        else:
            print('Course Type with given ID does not exist in the database')

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
    }
  }
} """

""" mutation {
  updateCourseType (
    id : "Q291cnNlVHlwZU5vZGU6MTc1"
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
    }
  }
} """