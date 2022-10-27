from distutils.command.build_scripts import first_line_re
import json
from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from people.models import Tutor
from base.models import Department



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
                                 tutor_info: Tutor,
                                 tutor_reseaux: Tutor):
    response_all_data = client_query(
        '''
        query {
          tutors {
            edges{
                node{
                    username
                }
            }
            }
        }
        '''
    )
    content_all_data = json.loads(response_all_data.content)
    assert 'errors' not in content_all_data
    all_tutors = content_all_data["data"]["tutors"]["edges"]
    assert len(all_tutors) == 2
    assert (set([tu["node"]["username"] for tu in all_tutors])
            == set([tut.username for tut in [tutor_info, tutor_reseaux]]))

def test_tutors_filt(client_query,
                                tutor_info: Tutor):
    response_filtered = client_query(
        '''
        query {
          tutors(firstName_Istartswith: "La") {
            edges {
                node {
                    email
                }
            }
          }
        }
        '''
    )
    content_filt = json.loads(response_filtered.content)
    assert 'errors' not in content_filt
    node = content_filt["data"]["tutors"]["edges"][0]["node"]["email"]
    assert node == tutor_info.email