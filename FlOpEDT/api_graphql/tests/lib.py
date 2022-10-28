import json
def test_all(client_query, obj_type, filter, filterValue, *fields, **fixtures):
    """
        Parameters :\n
        client_query : to execute the query\n
        obj_type (str): the type of the object\n
        filter (str): the filter function to use\n
        filterValue (préciser le type) : the value used to filter the results\n
        fields (argument.s) : fields appearing in the query\n
        fixtures (dict) : fixtures used to make the tests         
    """
    query = 'query { ' + obj_type
    
    if filter != None and filterValue != None:
        query += ' (' + filter + ': ' + filterValue + ') '

    query += ''' {
                edges{
                    node{
        '''

    for f in fields:
        query += f + ' '

    query += '''
                    }
                }
            }
        }        
    '''

    response = client_query(query)
    content = json.loads(response.content)
    assert 'errors' not in content
    all_elt = content["data"][obj_type]["edges"]
    assert len(all_elt) == len(fixtures)
    res = []
    for f in fields:
        res.extend([elt["node"][f] for elt in all_elt])

    fixt = []
    for f in fields:
        fixt.extend([getattr(e, f) for e in fixtures.values()])
    assert set(res) == set(fixt)