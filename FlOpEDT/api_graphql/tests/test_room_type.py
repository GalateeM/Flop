from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from base.models import RoomType, Department
from test_rooms import room_type_info, room_type_reseaux
from test_department import department_langues, department_info, department_reseaux
from lib import execute_query, get_data, execute_mutation, client_query
from graphql_relay import from_global_id, to_global_id

@pytest.fixture
def room_type_info2(db, \
    department_info : Department) -> RoomType:
    return RoomType.objects.create(
        department = department_info,
        name = "Salle de cours"
    )

# Query
def test_no_filter(client_query, room_type_info : RoomType, room_type_info2 : RoomType, room_type_reseaux : RoomType) :
    query = \
    """ query {
        roomTypes {
            edges {
                node {
                    name
                }
            }
        }
    }
    """       

    res = execute_query(client_query, query, "roomTypes")
    data = get_data(res)
    names = set([room_type_info.name, room_type_info2.name, room_type_reseaux.name])
    assert names == set(data["name"])

def test_filters(client_query, room_type_info2 : RoomType, room_type_info : RoomType):
    query = \
    """ query {
        roomTypes (department_Abbrev : "INFO", name_Icontains : "cours") {
            edges {
                node {
                    name
                }
            }
        }
    }
    """

    res = execute_query(client_query, query, "roomTypes")
    data = get_data(res)
    assert room_type_info2.name in data["name"]
    assert room_type_info.name not in data["name"]

# Mutations
def test_mutations (db, client_query, department_langues : Department, department_info : Department, capsys):
    department_info_id = to_global_id("Department", department_info.id)
    department_langues_id = to_global_id("Department", department_langues.id)    

    create = \
    """
        mutation {
            createRoomType (
                name : "Room Type 4"
                department : \"""" + department_info_id + \
        """\"               
            ) {
                roomTypes {
                    id
                }
            }
        }
    """

    global_id = execute_mutation(client_query, create, "createRoomType", "roomTypes")
    try:
        obj_id = from_global_id(global_id) [1]
        obj = RoomType.objects.get(id = obj_id)
        
        with capsys.disabled():
            print("The object was created successfully")
        
        update = \
    """
        mutation {
            updateRoomType (
                id : \"""" + global_id + \
        """\"   name : "Room Type 7"
                department : \"""" + department_langues_id + \
        """\"               
            ) {
                roomTypes {
                    id
                }
            }
        }
    """
        execute_mutation(client_query, update, "updateRoomType", "roomTypes")    
        obj_updated = RoomType.objects.get(id = obj_id)
        assert obj.name != obj_updated.name
        assert obj.department.name != obj_updated.department.name

        with capsys.disabled():
                print("The object was updated successfully")

        delete = """
        mutation {
            deleteRoomType ( 
                id : \"""" + global_id + \
                """\" ) {
                roomTypes {
                    id
                }
            }
            }
        """
        execute_mutation(client_query, delete, "deleteRoomType", "roomTypes")
        try:
            obj_deleted = RoomType.objects.get(id=obj_id)
            with capsys.disabled():
                print("The object was not deleted")
        except RoomType.DoesNotExist:
            with capsys.disabled():
                print("The object was deleted successfully")

    except RoomType.DoesNotExist:
        with capsys.disabled():
            print("The object was not created")
        assert False