from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from base.models import Department, GroupType
from test_course_type import department_info, department_langues, department_reseaux, group_type1, group_type4
from lib import execute_query, get_data, execute_mutation, client_query
from graphql_relay import from_global_id, to_global_id

@pytest.fixture
def group_type7(db, department_info : Department) -> GroupType:
    return GroupType.objects.create(
        name = "Group 7",
        department = department_info
    )

# Query
def test_no_filter(client_query, group_type1 : GroupType, group_type4 : GroupType):
    query = \
    """
        query {
            groupTypes {
                edges {
                    node {
                        name
                        department {
                            name
                        }
                    }
                }
            }
        }
    """
    res = execute_query(client_query, query, "groupTypes")
    data = get_data(res)
    assert set(data["name"]) == set([group_type1.name, group_type1.department.name, group_type4.name, group_type4.department.name])

def test_filter(client_query, group_type1 : GroupType, group_type7 : GroupType):
    query = \
    """
        query {
            groupTypes (name_Icontains : "7", department_Abbrev : "INFO") {
                edges {
                    node {
                        name
                    }
                }
            }
        }
    """
    res = execute_query(client_query, query, "groupTypes")
    data = get_data(res)
    assert group_type7.name in data["name"]
    assert group_type1.name not in data["name"]

# Mutations
def test_mutations(db, client_query, department_langues : Department, department_info : Department, capsys):
    department_info_id = to_global_id("Department", department_info.id)
    department_langues_id = to_global_id("Department", department_langues.id)

    create = \
    """ mutation {
        createGroupType (
            name : "Group Type 1"
            department : \"""" + department_info_id + \
    """\"    ) {
            groupType {
                id
            }      
        }
    }
    """

    global_id = execute_mutation(client_query, create, "createGroupType", "groupType")
    try:
        obj_id = from_global_id(global_id)[1]
        obj = GroupType.objects.get(id=obj_id)
        update = \
        """ mutation {
        updateGroupType (
            id : \"""" + global_id + \
            """\" name : "Group Type 7"
            department : \"""" + department_langues_id + \
    """\"    ) {
            groupType {
                id
            }      
        }
    }
        """
        execute_mutation(client_query, update, "updateGroupType", "groupType")
        obj_updated = GroupType.objects.get(id=obj_id)
        assert obj.name != obj_updated.name
        assert obj.department.name != obj_updated.department.name
        with capsys.disabled():
            print("The object was updated successfully")
        
        delete = """
        mutation {
            deleteGroupType ( 
                id : \"""" + global_id + \
                """\" ) {
                groupType {
                    id
                }
            }
            }
        """
        execute_mutation(client_query, delete, "deleteGroupType", "groupType")
        try:
            obj_deleted = GroupType.objects.get(id=obj_id)
            with capsys.disabled():
                print("The object was not deleted")
        
        except GroupType.DoesNotExist:
            with capsys.disabled():
                print("The object was deleted successfully")

    except GroupType.DoesNotExist:
        with capsys.disabled():
            print("The object was not created")
        assert False