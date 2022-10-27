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
    return Tutor.objects.create(abbrev="LN",  first_name="Laurent")


@pytest.fixture
def tutor_réseaux(db) -> Tutor:
    return Tutor.objects.create(abbrev="ADES",  first_name="Arnaud")




def departement_info_factory(db, tutor_info: Tutor):
    def create_department_info(
            abbrev: str,
            name:str)  -> department:
        return Department.objects.create(
            abbrev=abbrev, name=name,
            Tutor=tutor_info)
    return create_department_info
@pytest.fixture
def department_info(db, department_info_factory):
    return department_info_factory(abbrev="INFo", name="informatique")

@pytest.fixture
def department_réseaux(db, department_info_factory):
    return department_info_factory(abbrev="RT", name="réseaux et telecommunication")

# (Avec une List dans le type TrainingProgrammeQL)
def test_all_Tutors(client_query,
                                 tutor_info: Tutor,
                                 tutor_réseaux: Tutor):
    
    response = client_query(
        '''
        query {
          tutor(first_name_Istartswith: "La") {
            edges {
              node {
              first_name
              last_name
              username
              email
               
              }
            }
          }
        }
        '''
    )
    content = json.loads(response.content)
    assert 'errors' not in content
    # pas très nécessaire
    # assert "Tutors" in content["data"]
    Tutors = content["data"]["Tutors"]
    assert len(Tutors) == 1
    assert (set([tp["abbrev"] for tp in Tutors])
            == set([tp.abbrev for tp in [tutor_info, tutor_réseaux]]))

