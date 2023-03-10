from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from base.models import Week
from lib import execute_query, get_data, execute_mutation, client_query
from graphql_relay import from_global_id, to_global_id
from django.core.exceptions import ValidationError

@pytest.fixture
def week1(db) -> Week:
    week = Week.objects.create(nb=1, year=2022)
    try:
        week.full_clean()
    except ValidationError as e:
        print(e)
        pytest.fail("Erreur de validation lors de la création de l'objet Week")
    return week

@pytest.fixture
def week7(db) -> Week:
    week = Week.objects.create(nb=7, year=2021)
    try:
        week.full_clean()
    except ValidationError as e:
        print(e)
        pytest.fail("Erreur de validation lors de la création de l'objet Week")
    return week

# Query

def test_no_filter(client_query, week1 : Week, week7 : Week):
    query = \
    """
        query {
            weeks {
                edges {
                    node {
                        nb
                        year
                    }
                }
            }
        }
    """

    res = execute_query(client_query, query, "weeks")
    data = get_data(res)
    print("data")
    print(data)
    assert week1.nb in data["nb"]
    assert week1.year in data["year"]
    assert week7.nb in data["nb"]
    assert week7.year in data["year"]

# def test_filter(client_query, week1 : Week, week7 : Week):
#     query = \
#     """
#         query {
#             weeks (nb : 7) {
#                 edges {
#                     node {
#                         nb
#                         year
#                     }
#                 }
#             }
#         }
#     """

#     res = execute_query(client_query, query, "weeks")
#     data = get_data(res)
#     assert week1.nb not in data["nb"]
#     assert week1.year not in data["year"]
#     assert week7.nb in data["nb"]
#     assert week7.year in data["year"]

# # Mutation
# def test_mutations(db, client_query, capsys):
#     create = \
#     """
#         mutation {
#             createWeek (
#                 nb : 4
#                 year : 2023
#             ) {
#                 week {
#                     id
#                 }
#             }
#         }
#     """

#     global_id = execute_mutation(client_query, create, "createWeek", "week")
#     try:
#         obj_id = from_global_id(global_id)[1]
#         obj = Week.objects.get(id=obj_id)

#         with capsys.disabled():
#             print("The object was created successfully")

#         update = \
#         """
#             mutation {
#                 updateWeek (
#                     id : \"""" + global_id + \
#         """\"
#                     nb : 7
#                     year : 2022
#                 ) {
#                     week {
#                         id
#                     }
#                 }
#             }
#         """

#         execute_mutation(client_query, update, "updateWeek", "week")
#         obj_updated = Week.objects.get(id=obj_id)
#         assert obj.nb != obj_updated.nb
#         assert obj.year != obj_updated.year

#         with capsys.disabled():
#             print("The object was updated successfully")

#         delete = """
#         mutation {
#             deleteWeek ( 
#                 id : \"""" + global_id + \
#                 """\" ) {
#                 week {
#                     id
#                 }
#             }
#             }
#         """
#         execute_mutation(client_query, delete, "deleteWeek", "week")
#         try:
#             obj_deleted = Week.objects.get(id=obj_id)
#             with capsys.disabled():
#                 print("The object was not deleted")
#         except Week.DoesNotExist:
#             with capsys.disabled():
#                 print("The object was deleted successfully")

#     except Week.DoesNotExist:
#         with capsys.disabled():
#             print("The object was not created")
#         assert False