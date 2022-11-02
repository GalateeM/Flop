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
def tutor_info(db) -> Tutor:
    return Tutor.objects.create(username="LN",  first_name="Laurent")

@pytest.fixture
def tutor_reseaux(db) -> Tutor:
    return Tutor.objects.create(username="ADES",  first_name="Arnaud")
    
@pytest.fixture
def department_info(db) -> Department:
    return Department.objects.create(abbrev="INFO", name="informatique")

@pytest.fixture
def department_reseaux(db) -> Department:
    return Department.objects.create(abbrev="RT", name="reseaux et telecommunication")

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
    "username_Istartswith" : '"A"'
}

def test_tutors_one_filter(client_query,
                                tutor_info: Tutor):
    lib.test_all (client_query, "tutors", one_filter, "first_name", "username", t1 = tutor_info)

def test_tutors_multiple_filters(client_query,
                                tutor_reseaux: Tutor):
    lib.test_all (client_query, "tutors", multiple_filters, "first_name", "username", t1 = tutor_reseaux)    