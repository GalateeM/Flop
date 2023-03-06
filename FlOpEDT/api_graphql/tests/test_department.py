from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from base.models import Department
from test_course_type import department_langues, department_info, department_miashs, department_reseaux
from lib import execute_query, get_data, execute_mutation, client_query
from graphql_relay import from_global_id, to_global_id

""" Test Query
"""
def test_no_filter (client_query, department_langues : Department, department_info : Department, department_miashs : Department, department_reseaux : Department) :
    query = \
    """
        query{
            departments {
                edges {
                    node {
                        name
                    }
                }
            }
        }
    """
    res = execute_query(client_query, query, "departments")
    data = get_data(res)
    assert set([department_langues.name, department_info.name, department_miashs.name, department_reseaux.name]) ==  set(data["name"])

def test_with_filters (client_query, department_langues : Department, department_info : Department, department_miashs : Department, department_reseaux : Department) :
    query = \
    """
        query{
            departments (abbrev : "LNG") {
                edges {
                    node {
                        name
                    }
                }
            }
        }
    """
    res = execute_query(client_query, query, "departments")
    data = get_data(res)
    assert department_langues.name in data["name"]
    assert department_info not in data["name"]
    assert department_reseaux not in data["name"]
    assert department_miashs not in data["name"]

""" Test Mutations
"""
def test_mutations (db, client_query, capsys) :
    create = \
    """
        mutation {
            createDepartment (
                name : "Sociologie"
                abbrev : "SOC"
            ) {
                department {
                    id
                    abbrev
                }
            }
        }
    """

    global_id = execute_mutation(client_query, create, "createDepartment", "department")
    try:
        obj_id = from_global_id(global_id)[1]
        obj = Department.objects.get(id=obj_id)
        with capsys.disabled():
            print("The object was created successfully")

        update = """
            mutation {
                updateDepartment (
                    id : \"""" + global_id + \
                    """\" name : "Gestion"
                    abbrev : "GST"
                ) {
                department {
                    id
                    abbrev
                }
            }
        }
        """

        execute_mutation(client_query, update, "updateDepartment", "department")
        obj_updated = Department.objects.get(id=obj_id)
        assert obj.abbrev != obj_updated.abbrev
        assert obj.name != obj_updated.name
        with capsys.disabled():
            print("The object was updated successfully")

        delete = """
        mutation {
            deleteDepartment ( 
                id : \"""" + global_id + \
                """\" ) {
                department {
                    id
                }
            }
        }
        """
        execute_mutation(client_query, delete, "deleteDepartment", "department")
        try:
            obj_deleted = Department.objects.get(id=obj_id)
            with capsys.disabled():
                print("The object was not deleted")

        except Department.DoesNotExist:
            with capsys.disabled():
                print("The object was deleted successfully")


    except Department.DoesNotExist:
        with capsys.disabled():
            print("The object was not created")
        assert False
