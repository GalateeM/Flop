from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from base.models import Room, Department, RoomType
from test_tutor import department_info, department_reseaux
from lib import execute_query, get_data, execute_mutation, client_query
from graphql_relay import from_global_id, to_global_id

@pytest.fixture
def room_type_info(db, \
    department_info : Department) -> RoomType:
    return RoomType.objects.create(
        department = department_info,
        name = "Salle de conference"
    )

@pytest.fixture
def room_type_reseaux(db, \
    department_reseaux : Department) -> RoomType:
    return RoomType.objects.create(
        department = department_reseaux,
        name = "Salle de cours"
    )

@pytest.fixture
def room_reseaux(db, \
    department_reseaux : Department, \
    room_type_reseaux : RoomType) -> Room:
    res = Room.objects.create(
       name = "RT069"
    )
    res.save()
    res.departments.add(department_reseaux)
    res.types.add(room_type_reseaux)
    return res

@pytest.fixture
def room_info(db, \
    department_info : Department, \
    room_type_info : RoomType) -> Room:
    res = Room.objects.create(
       name = "INF407"
    )
    res.save()
    res.departments.add(department_info)
    res.types.add(room_type_info)
    return res

@pytest.fixture
def room_info_2(db, \
    department_info : Department, \
    room_type_info : RoomType) -> Room:
    res = Room.objects.create(
       name = "INF408"
    )
    res.save()
    res.departments.add(department_info)
    res.types.add(room_type_info)
    return res

# Query
def test_no_filter(client_query, room_info : Room, room_info_2 : Room, room_reseaux : Room):
    query = '''
        query {
            rooms {
                edges{
                    node{
                	    name
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "rooms")
    data = get_data(res) 
    names = set([room_info.name, room_info_2.name, room_reseaux.name])
    assert names == set(data["name"])

def test_filters(client_query, room_info : Room, room_info_2 : Room):
    query = '''
        query {
            rooms (name_Icontains : "7", dept : "INFO") {
                edges{
                    node{
                	    name
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "rooms")
    data = get_data(res) 
    assert room_info.name in data["name"]
    assert room_info_2.name not in data["name"]

# Mutation
def test_mutations(db, client_query, room_type_info : RoomType, room_type_reseaux : RoomType, room_reseaux : Room, room_info : Room, department_info : Department, department_reseaux : Department, capsys):
    room_type_info_id = to_global_id("RoomType", room_type_info.id)
    room_type_reseaux_id = to_global_id("RoomType", room_type_reseaux.id)
    room_reseaux_id = to_global_id("Room", room_reseaux.id)
    room_info_id = to_global_id("Room", room_info.id)
    department_info_id = to_global_id("Department", department_info.id)
    department_reseaux_id = to_global_id("Department", department_reseaux.id)

    create = \
    """
        mutation {
            createRoom (
                name : "Room 11"
                types : [\"""" + room_type_info_id + \
    """\"]      subroomOf : [\"""" + room_info_id + \
    """\"]      departments : [\"""" + department_info_id + \
    """\"]
            ) {
                rooms {
                    id
                }
            }
        }
    """
    print(create)
    global_id = execute_mutation(client_query, create, "createRoom", "rooms")
    try:
        obj_id = from_global_id(global_id)[1]
        obj = Room.objects.get(id=obj_id)
        types_obj = []
        for t in obj.types.all():
            types_obj.append(t.name)
        subroom_of_obj = []
        for s in obj.subroom_of.all():
            subroom_of_obj.append(s.name)
        depts_obj = []
        for d in obj.departments.all():
            depts_obj.append(d.name)

        with capsys.disabled():
            print("The object was created successfully")
        update = \
        """
        mutation {
            updateRoom (
            id : \"""" + global_id + \
    """\"   name : "Room 77"
                types : [\"""" + room_type_reseaux_id + \
    """\"]      subroomOf : [\"""" + room_reseaux_id + \
    """\"]      departments : [\"""" + department_reseaux_id + \
    """\"]
            ) {
                rooms {
                    id
                }
            }
        }
    """

        execute_mutation(client_query, update, "updateRoom", "rooms")
        obj_updated = Room.objects.get(id=obj_id)
        assert obj.name != obj_updated.name
        
        types_obj_updated = []
        for t in obj_updated.types.all():
            types_obj_updated.append(t.name)
        subroom_of_obj_updated = []
        for s in obj_updated.subroom_of.all():
            subroom_of_obj_updated.append(s.name)
        depts_obj_updated = []
        for d in obj_updated.departments.all():
            depts_obj.append(d.name)
        
        assert set(types_obj) != set(types_obj_updated)
        assert set(subroom_of_obj) != set(subroom_of_obj_updated)
        assert set(depts_obj) != set(depts_obj_updated)

        with capsys.disabled():
            print("The object was updated successfully")

        delete = """
        mutation {
            deleteRoom ( 
                id : \"""" + global_id + \
                """\" ) {
                rooms {
                    id
                }
            }
            }
        """
        execute_mutation(client_query, delete, "deleteRoom", "rooms")
        try:
            obj_deleted = Room.objects.get(id=obj_id)
            with capsys.disabled():
                print("The object was not deleted")
        except Room.DoesNotExist:
            with capsys.disabled():
                print("The object was deleted successfully")

    except Room.DoesNotExist:
        with capsys.disabled():
            print("The object was not created")
        assert False