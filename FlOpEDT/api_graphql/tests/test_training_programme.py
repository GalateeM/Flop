from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from graphql_relay import from_global_id, to_global_id

from base.models import TrainingProgramme, Department

from lib import execute_query, get_data, execute_mutation, client_query
from test_department import department_miashs, department_langues
from test_modules import training_l2_miashs, training_l3_miashs


@pytest.fixture
def training_m1_langues(db, department_langues: Department) -> TrainingProgramme:
    return TrainingProgramme.objects.create(
        abbrev="M1L", name="M1 LANGUES",
        department=department_langues)

# Query
def test_filter_dept(client_query, training_l2_miashs : TrainingProgramme, training_l3_miashs : TrainingProgramme, training_m1_langues : TrainingProgramme):
    query = \
    """
        query {
            trainingProgrammes (dept : "LNG") {
                edges {
                    node {
                        name
                    }
                }
            }
        }
    """

    res = execute_query(client_query, query, "trainingProgrammes")
    data = get_data(res)
    assert training_m1_langues.name in data["name"]
    assert training_l2_miashs.name not in data["name"]
    assert training_l3_miashs.name not in data["name"]

def test_filters(client_query, training_l2_miashs : TrainingProgramme, training_l3_miashs : TrainingProgramme):
    query = \
    """
        query {
            trainingProgrammes (dept : "MIASHS", abbrev : "L3M") {
                edges {
                    node {
                        name
                    }
                }
            }
        }
    """

    res = execute_query(client_query, query, "trainingProgrammes")
    data = get_data(res)
    assert training_l2_miashs.name not in data["name"]
    assert training_l3_miashs.name in data["name"]

# Mutation
def test_mutations(db, client_query, department_miashs : Department, department_langues : Department, capsys):
    department_miashs_id = to_global_id("Department", department_miashs.id) 
    department_langues_id = to_global_id("Department", department_langues.id)
    
    create = \
    """
        mutation {
            createTrainingProgramme (
                name : "Training Miashs"
                abbrev : "TM"
                department : \"""" + department_miashs_id + \
    """\"       
            ) {
                trainingProgramme {
                    id
                }
            }
        }
    """

    global_id = execute_mutation(client_query, create, "createTrainingProgramme", "trainingProgramme")
    try:
        obj_id = from_global_id(global_id)[1]
        obj = TrainingProgramme.objects.get(id=obj_id)

        with capsys.disabled():
            print("The object was created successfully")
        
        update = """
            mutation {
                updateTrainingProgramme (
                    id : \"""" + global_id + \
        """\" name : "Training Langues"
                    abbrev : "TL"
                    department : \"""" + department_langues_id + \
        """\"       
            ) {
                trainingProgramme {
                    id
                }
            }
        } 
        """

        execute_mutation(client_query, update, "updateTrainingProgramme", "trainingProgramme")
        obj_updated = TrainingProgramme.objects.get(id=obj_id)
        assert obj.name != obj_updated.name
        assert obj.abbrev != obj_updated.abbrev
        assert obj.department.abbrev != obj_updated.department.abbrev

        with capsys.disabled():
            print("The object was updated successfully")

        delete = """
            mutation {
                deleteTrainingProgramme (
                    id : \"""" + global_id + \
        """\" ) {
                trainingProgramme {
                    id
                }
            }
        }
        """
        execute_mutation(client_query, delete, "deleteTrainingProgramme", "trainingProgramme")
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