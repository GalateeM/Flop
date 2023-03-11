from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from quote.models import QuoteType
from test_quote import quote_type1, quote_type2
from lib import execute_query, get_data, execute_mutation, client_query
from graphql_relay import from_global_id, to_global_id

@pytest.fixture
def quote_type3(db, quote_type1 : QuoteType) -> QuoteType:
    return QuoteType.objects.create(name="drole", abbrev="DR2", parent = quote_type1)

# Query
def test_no_filter(client_query, quote_type1 : QuoteType, quote_type2 : QuoteType, quote_type3 : QuoteType):
    query = \
    """
        query {
            quoteTypes {
                edges {
                    node {
                        name
                    }
                }
            }
        }
    """

    res = execute_query(client_query, query, "quoteTypes")
    data = get_data(res)
    names = set([quote_type1.name, quote_type3.name, quote_type2.name])
    assert names == set(data["name"])

def test_filters(client_query, quote_type3 : QuoteType, quote_type1 : QuoteType):
    query = \
    """
        query {
            quoteTypes (name_Icontains : "drole", parent_Name_Icontains : "dr") {
                edges {
                    node {
                        abbrev
                    }
                }
            }
        }
    """

    res = execute_query(client_query, query, "quoteTypes")
    data = get_data(res)
    assert quote_type3.abbrev in data["abbrev"]
    assert quote_type1.abbrev not in data["abbrev"]

# Mutation
def test_mutations(db, client_query, quote_type1 : QuoteType, quote_type2 : QuoteType, capsys):
    quote_type1_id = to_global_id("QuoteType", quote_type1.id)
    quote_type2_id = to_global_id("QuoteType", quote_type2.id)

    create = \
    """
        mutation {
            createQuoteType (
                name : "Quote Type 4"
                abbrev : "QT4"
                parent : \"""" + quote_type1_id + \
    """\"         
            ) {
                quoteTypes {
                   id
                }
            }
        }
    """

    global_id = execute_mutation(client_query, create, "createQuoteType", "quoteTypes")
    try:
        obj_id = from_global_id(global_id)[1]
        obj = QuoteType.objects.get(id=obj_id)
        with capsys.disabled():
            print("The object was created successfully")
        
        update = \
        """
            mutation {
            updateQuoteType (
                id : \"""" + global_id + \
        """\"   name : "Quote Type 7"
                abbrev : "QT7"
                parent : \"""" + quote_type2_id + \
    """\"         
            ) {
                quoteTypes {
                    id
                }
            }
        }
        """

        execute_mutation(client_query, update, "updateQuoteType", "quoteTypes")
        obj_updated = QuoteType.objects.get(id=obj_id)
        assert obj.name != obj_updated.name
        assert obj.abbrev != obj_updated.abbrev
        assert obj.parent.abbrev != obj_updated.parent.abbrev

        with capsys.disabled():
            print("The object was updated successfully")

        delete = """
        mutation {
            deleteQuoteType ( 
                id : \"""" + global_id + \
                """\" ) {
                 quoteTypes {
                    id
                }
            }
            }
        """
        execute_mutation(client_query, delete, "deleteQuoteType", "quoteTypes")
        try:
            obj_deleted = QuoteType.objects.get(id=obj_id)
            with capsys.disabled():
                print("The object was not deleted")
        except QuoteType.DoesNotExist:
            with capsys.disabled():
                print("The object was deleted successfully")

    except QuoteType.DoesNotExist:
        with capsys.disabled():
            print("The object was not created")
        assert False