from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from base.models import Period , Department
from test_course_type import department_miashs, department_langues
from lib import execute_query, get_data, execute_mutation, client_query
from graphql_relay import from_global_id, to_global_id

@pytest.fixture
def period_1 (db, department_miashs : Department) -> Period:
    return Period.objects.create(
        name = "Period 1",
        department = department_miashs,
        starting_week = 4,
        ending_week = 7
    )

@pytest.fixture
def period_2 (db, department_miashs : Department) -> Period:
    return Period.objects.create(
        name = "Period 2",
        department = department_miashs,
        starting_week = 7,
        ending_week = 11
    )

@pytest.fixture
def period_3 (db, department_langues : Department) -> Period:
    return Period.objects.create(
        name = "Period 3",
        department = department_langues,
        starting_week = 11,
        ending_week = 20
    )

# Query
def test_no_filter (client_query, period_1 : Period, period_2 : Period, period_3 : Period):
    query = \
    """ 
        query {
            periods {
                edges {
                    node {
                        name
                        department {
                            name
                        }
                        startingWeek
                        endingWeek
                    }
                }
            }
        }
    """
    res = execute_query(client_query, query, "periods")
    data = get_data(res)
    names = [period_1.name, period_1.department.name, period_2.name, period_2.department.name, period_3.name, period_3.department.name]
    assert set(names) == set(data["name"])
    assert period_1.starting_week in data["startingWeek"]
    assert period_1.ending_week in data["endingWeek"]
    assert period_2.starting_week in data["startingWeek"]
    assert period_2.ending_week in data["endingWeek"]
    assert period_3.starting_week in data["startingWeek"]
    assert period_3.ending_week in data["endingWeek"]

def test_filter (client_query, period_1 : Period, period_2 : Period):
    query = \
    """ 
        query {
            periods (name_Icontains : "1", department_Abbrev : "MIASHS") {
                edges {
                    node {
                        name
                    }
                }
            }
        }
    """
    res = execute_query(client_query, query, "periods")
    data = get_data(res)
    assert period_1.name in data["name"]
    assert period_2.name not in data["name"]

# Mutations
def test_mutations(db, client_query, department_miashs : Department, department_langues : Department, capsys):
    department_miashs_id = to_global_id("Department", department_miashs.id)
    department_langues_id = to_global_id("Department", department_langues.id)

    create = \
    """ 
        mutation {
            createPeriod (
                name : "Period 11"
                department : \"""" + department_miashs_id + \
    """\"       startingWeek : 10
                endingWeek : 17     
        ) {
            period {
                id
            }
        }
    }
    """

    global_id = execute_mutation(client_query, create, "createPeriod", "period")
    try:
        obj_id = from_global_id(global_id)[1]
        obj = Period.objects.get(id=obj_id)
        with capsys.disabled():
            print("The object was created successfully")
        
        update = \
        """ 
        mutation {
            updatePeriod (
                id : \"""" + global_id + \
    """\"          name : "Period 5"
                department : \"""" + department_langues_id + \
    """\"       startingWeek : 6
                endingWeek : 10     
        ) {
            period {
                id
            }
        }
    }
    """
        execute_mutation(client_query, update, "updatePeriod", "period")
        obj_updated = Period.objects.get(id=obj_id)
        assert obj.name != obj_updated.name
        assert obj.starting_week != obj_updated.starting_week
        assert obj.ending_week != obj_updated.ending_week
        assert obj.department.name != obj_updated.department.name
        with capsys.disabled():
            print("The object was updated successfully")
        
        delete = """
        mutation {
            deletePeriod ( 
                id : \"""" + global_id + \
                """\" ) {
                period {
                    id
                }
            }
            }
        """
        execute_mutation(client_query, delete, "deletePeriod", "period")
        try:
            obj_deleted = Period.objects.get(id=obj_id)
            with capsys.disabled():
                print("The object was not deleted")
        except Period.DoesNotExist:
            with capsys.disabled():
                print("The object was deleted successfully")

    except Period.DoesNotExist:
        with capsys.disabled():
            print("The object was not created")
        assert False