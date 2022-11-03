from distutils.command.build_scripts import first_line_re
import json
from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from people.models import Tutor
from base.models import Department
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
    "firstName_Icontains" : '"a"',
    "departments_Abbrev" : '"RT"'
}

def test_tutors_one_filter(client_query,
                                tutor_info: Tutor):
    lib.test_all (client_query, "tutors", one_filter, "first_name", "username", t1 = tutor_info)

def test_tutors_multiple_filters(client_query,
                                tutor_reseaux: Tutor):
    lib.test_all (client_query, "tutors", multiple_filters, "first_name", "username", t1 = tutor_reseaux)    