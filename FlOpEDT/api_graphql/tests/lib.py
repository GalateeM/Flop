import json

def test_all(client_query, obj_type, comp, filter, filterValue, *fields, **fixtures):
    """
        Parameters :\n
        client_query : to execute the query\n
        obj_type (str): the type of the object\n
        comp (str): field used to make the comparison\n
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
    assert (set([elt["node"][comp] for elt in all_elt])
            == set([getattr(e, comp) for e in fixtures.values()]))