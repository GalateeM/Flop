from distutils.command.build_scripts import first_line_re
import json
from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from people.models import Tutor
from base.models import Department, Week, ModuleTutorRepartition
import lib



@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs,
                             client=client,
                             graphql_url="/graphql")

    return func

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
"""
@pytest.fixture
def tutor_rand(db) -> Tutor:
    res = Tutor.objects.create(username="RD",  first_name="Random")
    return res

@pytest.fixture
def week1(db) -> Week:
    return Week.objects.create(nb=1, year=2022)

@pytest.fixture
def week7(db) -> Week:
    return Week.objects.create(nb=7, year=2021)

@pytest.fixture
def mod_rep_info(db, week1 : Week, tutor_info : Tutor) -> ModuleTutorRepartition:
    return ModuleTutorRepartition(
        module = None,
        course_type = None,
        tutor = tutor_info,
        week = week1,
        courses_nb = None
    )

@pytest.fixture
def mod_rep_reseaux(db, week7 : Week, tutor_reseaux : Tutor) -> ModuleTutorRepartition:
    return ModuleTutorRepartition(
        module = None,
        course_type = None,
        tutor = tutor_reseaux,
        week = week7,
        courses_nb = None
    )

@pytest.fixture
def mod_rep_random(db, week7 : Week) -> ModuleTutorRepartition:
    return ModuleTutorRepartition(
        module = None,
        course_type = None,
        tutor = tutor_rand,
        week = week7,
        courses_nb = None
    )
"""
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
    res = lib.execute_query (client_query, query, "tutors")
    data = lib.get_data(res)
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
    res = lib.execute_query (client_query, query, "tutors")
    data = lib.get_data(res)
    assert tutor_info.first_name in data["firstName"]
    assert tutor_info.username in data["username"]



"""
multiple_filters = {
    "week_Nb" : '7',
    "tutor_FirstName_Icontains" : '"a"',
    "tutor_Departments_Abbrev" : '"RT"'
}

def test_tutors_multiple_filters(client_query,
                                tutor_reseaux: Tutor):
    lib.test_all (client_query, "tutors", multiple_filters, {"tutor" : ["first_name", "username"]}, t1 = tutor_reseaux)


def test_all_tutors(client_query,
                    tutor_info : Tutor, 
                    tutor_reseaux : Tutor):
    lib.test_all (client_query, "tutors", None, "username", 
    t1 = tutor_info,
    t2 = tutor_reseaux)

one_filter = {
    "firstName_Istartswith" : '"La"'
}

multiple_filters = {
    "week_nb" : '7',
    "firstName_Icontains" : '"a"',
    "departments_Abbrev" : '"RT"'
}

def test_tutors_one_filter(client_query,
                                tutor_info: Tutor):
    lib.test_all (client_query, "tutors", one_filter, "first_name", "username", t1 = tutor_info)

def test_tutors_multiple_filters(client_query,
                                tutor_reseaux: Tutor):
    lib.test_all (client_query, "tutors", multiple_filters, "first_name", "username", t1 = tutor_reseaux)
"""

    