from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query

from lib import execute_query, get_data, client_query


def test_filter(db, client_query):
    query = \
    """
        query {
            weeks (nb : 7, year : 2021) {
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
    assert len (data["nb"]) == len (data["year"]) == 1
    assert 7 in data["nb"]
    assert 2021 in data["year"]