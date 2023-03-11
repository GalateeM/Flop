from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from graphql_relay import from_global_id, to_global_id

from people.models import Tutor
from base.models import ScheduledCourse, Department

from lib import execute_query, get_data, execute_mutation, client_query
from test_scheduled_course import week1, week7, module_algo_prog, module_conception_log, training_l3_miashs ,training_l2_miashs, \
department_miashs, period_1 , period_2, tutor_algo_prog, tutor_conception, \
course_type_algo, room_algo, course_algo, scheduled1, \
course_type_conception, room_conception, course_conception, scheduled2


@pytest.fixture
def department_info(db) -> Department:
    return Department.objects.create(abbrev="INFO", name="informatique")

@pytest.fixture
def department_reseaux(db) -> Department:
    return Department.objects.create(abbrev="RT", name="reseaux et telecommunication")

@pytest.fixture
def tutor_info(db, department_info : Department) -> Tutor:
    res = Tutor.objects.create(username="LN",  first_name="Laurent")
    res.save()
    res.departments.add(department_info)
    res.save()
    return res

@pytest.fixture
def tutor_reseaux(db, department_reseaux : Department) -> Tutor:
    res = Tutor.objects.create(username="ADES",  first_name="Arnaud")
    res.save()
    res.departments.add(department_reseaux)
    res.save()
    return res

# Query
def test_all_tutors_dept(client_query,
                    tutor_info : Tutor, 
                    tutor_reseaux : Tutor):
    query='''
        query {
            tutors (dept : \"RT\") {
                edges {
                    node {
                        username
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "tutors")
    data = get_data(res)
    assert tutor_reseaux.username in data["username"]
    assert tutor_info.username not in data["username"]

def test_tutors_algo(client_query,
                           tutor_algo_prog: Tutor, scheduled1 : ScheduledCourse, scheduled2 : ScheduledCourse):
    query='''
        query {
            tutors (dept : \"MIASHS\", week : 7, year : 2021){
                edges {
                    node {
                        username
                        firstName
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "tutors")
    data = get_data(res)
    assert tutor_algo_prog.first_name in data["firstName"]
    assert tutor_algo_prog.username in data["username"]
    
# Mutations
def test_mutations(db, client_query, department_miashs : Department, department_info : Department, department_reseaux : Department, capsys):
    dpt_info_id = to_global_id('Department', department_info.id)
    dpt_reseaux_id = to_global_id('Department', department_reseaux.id)
    dpt_miashs_id = to_global_id('Department', department_miashs.id)
    create = """
        mutation {
            createTutor (
                username : "usr1"
                firstName : "fst1"
                lastName : "lst1"
                email : "fts1.lst1@mail.com"
                password : "azerty"
                departments : [\"""" + dpt_info_id + "\", \"" + dpt_reseaux_id + \
                """\"] ) {
                tutor {
                    id
                }
                departments{
                  id
                  abbrev
                }
            }
            }
    """

    global_id = execute_mutation(client_query, create, "createTutor", "tutor")
    try:
        obj_id = from_global_id(global_id)[1]
        obj = Tutor.objects.get(id=obj_id)
        departments_obj = []
        for d in obj.departments.all():
            departments_obj.append(d.name)
        
        with capsys.disabled():
            print("The object was created successfully")
        
        update = """
        mutation {
            updateTutor ( 
                id : \"""" + global_id + \
                """\" username : "usr2"
                isActive : false
                departments : [\"""" + dpt_miashs_id + \
                """\"] ) {
                tutor {
                    id
                }
                departments{
                  id
                  abbrev
                }
            }
            }
        """

        execute_mutation(client_query, update, "updateTutor", "tutor")
        obj_updated = Tutor.objects.get(id=obj_id)
        assert obj.username != obj_updated.username 
        assert obj.is_active != obj_updated.is_active
        departments_obj_updated = []
        for d in obj_updated.departments.all():
            departments_obj_updated.append(d.name)
        assert set(departments_obj) != set(departments_obj_updated)
        with capsys.disabled():
            print("The object was updated successfully")

        delete = """
        mutation {
            deleteTutor ( 
                id : \"""" + global_id + \
                """\" ) {
                tutor {
                    id
                }
            }
            }
        """
        execute_mutation(client_query, delete, "deleteTutor", "tutor")
        try:
            obj_deleted = Tutor.objects.get(id=obj_id)
            with capsys.disabled():
                print("The object was not deleted")
        except Tutor.DoesNotExist:
            with capsys.disabled():
                print("The object was deleted successfully")


    except Tutor.DoesNotExist:
        with capsys.disabled():
            print("The object was not created")
        assert False