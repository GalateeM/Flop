import json
from people.models import Tutor 

def normalize_field_name(f):
    if "_" in f:
        l = f.rsplit("_")
        return l[0] + (l[1][0]).upper() + (l[1][1:])
    else:
        return f

def test_all(client_query, obj_type, filters, *fields, **fixtures):
    """
        Parameters :\n
        client_query : to execute the query\n
        obj_type (str): the type of the object\n
        filters (dict): filter(s) function(s) with their value(s)\n
        fields (argument.s) : fields appearing in the query\n
        fixtures (dict) : fixtures used to make the tests         
    """
    normalized_field_name = [normalize_field_name(f) for f in fields]
    query = 'query { ' + obj_type
    
    if filters != None:
        query += ' (' 
        for (fct, val) in filters.items():
            query += fct + ': ' + val + ", "
                
        query = query[:-2] + ') '

    query += ''' {
                edges{
                    node{
        '''
    
    if type (fields[0]) != dict :
        for f in normalized_field_name:
            query += f + ' '

        query += ' }   }   }   } '
    else:
        for f in normalized_field_name:
            for k, v in f.items():
                query += k + ' { '
                for vals in v:
                    query += vals + ' '
            query += ' } '
        query += ' }    }   } '

    response = client_query(query)
    content = json.loads(response.content)
    print(content["data"])
    assert False
    """
    assert 'errors' not in content
    all_elt = content["data"][obj_type]["edges"]
    assert len(all_elt) == len(fixtures)
    res = []
    for f in normalized_field_name:
        res.extend([elt["node"][f] for elt in all_elt])
    fixt = []
    for f in fields:
        fixt.extend([getattr(e, f) for e in fixtures.values()])
    assert set(res) == set(fixt)
"""