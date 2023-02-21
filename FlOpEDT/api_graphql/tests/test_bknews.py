from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from displayweb.models import BreakingNews
from base.models import Department, Week, ModuleTutorRepartition
from test_tutor import department_info, department_reseaux
from lib import execute_query, get_data, execute_mutation, client_query
from graphql_relay import from_global_id, to_global_id

# #parametre test
# @pytest.fixture
# def y1(db, department_info:Department) -> BreakingNews:
#     return BreakingNews.objects.create(department= department_info , week = 11, year = 2021,y=5, txt = "Lorem ipsum dolor sit amet.")

# @pytest.fixture
# def y2(db, department_reseaux:Department) -> BreakingNews:
#     return BreakingNews.objects.create(department= department_reseaux,week = 15, year = 2022, y=10, txt = "In atque alias et eveniet provident eos")

# def test_bknews(client_query,
#                     y1 : BreakingNews,
#                     y2 : BreakingNews):
#     query='''
#         query{
#             bknews {
#                 edges {
#                     node {
#                         y
#                         txt
#                     }
#                 }ef execute_mutation(client_query, query, mutationName, modelName):
#     response = client_query(query)
#     content = json.loads(response.content)
#     """ print(content)
#     assert False """
#     assert "errors" not in content
#     return content["data"][mutationName][modelName]["id"]
#             }
#         }
#     '''
#     res = execute_query (client_query, query, "bknews")
#     data = get_data(res)
#     assert y1.y in data["y"]
#     assert y2.y in data["y"]
#     assert y1.txt in data["txt"]
#     assert y2.txt in data["txt"]

# def test_bknews_filters1(client_query,
#                     y1 : BreakingNews):
#     query='''
#         query{
#             bknews (department_Name_Istartswith : \"inf\", week : 11, year : 2021, y : 5) {
#                 edges {
#                     node {
#                         txt
#                     }
#                 }
#             }
#         }
#     '''
#     res = execute_query (client_query, query, "bknews")
#     data = get_data(res)
#     assert y1.txt in data["txt"]

""" Tests mutations
"""
def test_mutations(db, client_query, department_info : Department, capsys):
    dpt_info_id = to_global_id('Department', department_info.id)
    create = """
        mutation {
            createBknews ( 
                year : 2024
                txt : "blablablabla"
                week : 2
                department : \"""" + dpt_info_id + \
            """\" ) {
                bknews {
                id
                }
            }
            }
    """

    global_id = execute_mutation(client_query, create, "createBknews", "bknews")
    try:
        obj_id = from_global_id(global_id)[1]
        obj = BreakingNews.objects.get(id=obj_id)
        with capsys.disabled():
            print("The object was created successfully")
        update = """
        mutation {
            updateBknews ( 
                id : \"""" + global_id + \
                """\" year : 2023
                txt : "blibliblibli"
                week : 7
            ) {
                bknews {
                id
                }
            }
            }
        """

        execute_mutation(client_query, update, "updateBknews", "bknews")
        obj_updated = BreakingNews.objects.get(id=obj_id)
        upd = (obj.year != obj_updated.year) and (obj.txt != obj_updated.txt) and (obj.week != obj_updated.week)
        assert upd
        if upd:
            with capsys.disabled():
                print("The object was updated successfully")
        else:
            with capsys.disabled():
                print("The object was not updated")

        delete = """
        mutation {
            deleteBknews ( 
                id : \"""" + global_id + \
                """\" ) {
                bknews {
                id
                }
            }
            }
        """
        execute_mutation(client_query, delete, "deleteBknews", "bknews")
        try:
            obj_deleted = BreakingNews.objects.get(id=obj_id)
            with capsys.disabled():
                print("The object was not deleted")
        except BreakingNews.DoesNotExist:
            with capsys.disabled():
                print("The object was deleted successfully")


    except BreakingNews.DoesNotExist:
        with capsys.disabled():
            print("The object was not created")
        assert False