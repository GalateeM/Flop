from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from people.models import Tutor
from base.models import Department, Week, ModuleTutorRepartition
from lib import *

@pytest.fixture
def department_info(db) -> Department:
    return Department.objects.create(abbrev="INFO", name="informatique")

@pytest.fixture
def department_reseaux(db) -> Department:
    return Department.objects.create(abbrev="RT", name="reseaux et telecommunication")

@pytest.fixture
def tutor_info(db, department_info : Department) -> Tutor:
    res = Tutor.objects.create(username="LN",  first_name="Laurent")
    res.departments.add(department_info)
    return res

@pytest.fixture
def tutor_reseaux(db, department_reseaux : Department) -> Tutor:
    res = Tutor.objects.create(username="ADES",  first_name="Arnaud")
    res.departments.add(department_reseaux)
    return res

def test_all_tutors(client_query,
                    tutor_info : Tutor, 
                    tutor_reseaux : Tutor):
    query='''
        query {
            tutors {
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
    assert tutor_info.username in data["username"]
    assert tutor_reseaux.username in data["username"]

def test_tutors_one_filter(client_query,
                           tutor_info: Tutor):
    query='''
        query {
            tutors (firstName_Istartswith : \"la\"){
                edges {
                    node {
                        firstName
                        username
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "tutors")
    data = get_data(res)
    assert tutor_info.first_name in data["firstName"]
    assert tutor_info.username in data["username"]
    
