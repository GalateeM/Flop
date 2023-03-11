from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from graphql_relay import from_global_id, to_global_id

from quote.models import Quote, QuoteType

from lib import execute_query, get_data, execute_mutation, client_query


@pytest.fixture
def quote_type1(db) -> QuoteType:
    return QuoteType.objects.create(name="drole", abbrev="DR")

@pytest.fixture
def quote_type2(db) -> QuoteType:
    return QuoteType.objects.create(name="serieux", abbrev="SE")


@pytest.fixture
def quote1(db, quote_type1:QuoteType) -> Quote:
    return Quote.objects.create(quote="Si la connerie se mesurait, tu servirais de metre-etalon. Tu serais a Sevres.", date="20 juillet 2020", quote_type = quote_type1)

@pytest.fixture
def quote2(db, quote_type2:QuoteType) -> Quote:
    return Quote.objects.create(quote="Trop gesticuler mene au ridicule.", date="16 fevrier 1968", quote_type = quote_type2)

# Query
def test_quote(client_query,
                quote1 : Quote,
                quote2 : Quote):
    query='''
        query {
            quotes {
                edges {
                    node {
                        id
                        quote
                        date
                        quoteType{
                            name
                            abbrev
                        }
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "quotes")
    data = get_data(res)
    assert quote1.quote in data["quote"]
    assert quote1.date in data["date"]
    assert quote1.quote_type.name in data["name"]
    assert quote1.quote_type.abbrev in data["abbrev"]
    assert quote2.quote in data["quote"]
    assert quote2.date in data["date"]
    assert quote2.quote_type.name in data["name"]
    assert quote2.quote_type.abbrev in data["abbrev"]

def test_quote_filter(client_query,
                quote2 : Quote):
    query='''
        query {
            quotes (date_Istartswith : \"16\") {
                edges {
                    node {
                        id
                        quote
                        date
                        quoteType {
                            name
                            abbrev
                        }
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "quotes")
    data = get_data(res)
    assert quote2.quote in data["quote"]
    assert quote2.date in data["date"]
    assert quote2.quote_type.name in data["name"]
    assert quote2.quote_type.abbrev in data["abbrev"]

# Mutation
def test_mutations (db, client_query, quote_type1 : QuoteType, quote_type2 : QuoteType, capsys):
    quote_type1_id = to_global_id("QuoteType", quote_type1.id)
    quote_type2_id = to_global_id("QuoteType", quote_type2.id)

    create = \
    """
        mutation {
            createQuote (
                quote : "Azertyuiop"
                quoteType : \"""" + quote_type1_id + \
    """\"
            ) {
                quotes {
                    id
                }
            }
        }
    """

    global_id = execute_mutation(client_query, create, "createQuote", "quotes")
    try:
        obj_id = from_global_id(global_id)[1]
        obj = Quote.objects.get(id=obj_id)
        with capsys.disabled():
            print("The object was created successfully")

        update = \
    """
        mutation {
            updateQuote (
                id :\"""" + global_id + \
    """\"       quote : "Qsdfghjklm"
                quoteType : \"""" + quote_type2_id + \
    """\"
            ) {
                quotes {
                    id
                }
            }
        }
    """

        execute_mutation(client_query, update, "updateQuote", "quotes")
        obj_updated = Quote.objects.get(id=obj_id)
        assert obj.quote != obj_updated.quote
        assert obj.quote_type.name != obj_updated.quote_type.name

        with capsys.disabled():
            print("The object was updated successfully")

        delete = """
        mutation {
            deleteQuote ( 
                id : \"""" + global_id + \
                """\" ) {
                quotes {
                    id
                }
            }
            }
        """
        execute_mutation(client_query, delete, "deleteQuote", "quotes")
        try:
            obj_deleted = Quote.objects.get(id=obj_id)
            with capsys.disabled():
                print("The object was not deleted")
        except Quote.DoesNotExist:
            with capsys.disabled():
                print("The object was deleted successfully")

    except Quote.DoesNotExist:
        with capsys.disabled():
            print("The object was not created")
        assert False