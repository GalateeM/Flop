from distutils.command.build_scripts import first_line_re
import json
from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from displayweb.models import BreakingNews
from base.models import Department, Week, ModuleTutorRepartition
from api_graphql.tests.test_modules import client_query as client_query
from api_graphql.tests.test_tutor import department_info as department_info, \
department_reseaux as department_reseaux
import lib




#parametre test
@pytest.fixture
def y1(db, department_info:Department) -> BreakingNews:
    return BreakingNews.objects.create(department= department_info , week = 11, year = 2021,y=5, txt = "Lorem ipsum dolor sit amet.")

@pytest.fixture
def y2(db, department_reseaux:Department) -> BreakingNews:
    return BreakingNews.objects.create(department= department_reseaux,week = 15, year = 2022, y=10, txt = "In atque alias et eveniet provident eos")

def test_bknews(client_query,
                    y1 : BreakingNews,
                    y2 : BreakingNews):
    query='''
        query{
            bknews {
                edges {
                    node {
                        y
                        txt
                    }
                }
            }
        }
    '''
    res = lib.execute_query (client_query, query, "bknews")
    data = lib.get_data(res)
    assert y1.y in data["y"]
    assert y2.y in data["y"]
    assert y1.txt in data["txt"]
    assert y2.txt in data["txt"]

def test_bknews_filters1(client_query,
                    y1 : BreakingNews):
    query='''
        query{
            bknews (department_Name_Istartswith : \"inf\", week : 1, year : 2021, y : 5) {
                edges {
                    node {
                        txt
                    }
                }
            }
        }
    '''
    res = lib.execute_query (client_query, query, "bknews")
    data = lib.get_data(res)
    assert y1.txt in data["txt"]