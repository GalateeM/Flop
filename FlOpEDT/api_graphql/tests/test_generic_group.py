from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from graphql_relay import from_global_id, to_global_id

from base.models import TrainingProgramme, Department, GroupType, GenericGroup

from lib import execute_query, get_data, execute_mutation, client_query
from test_modules import training_l2_miashs, training_l3_miashs
from test_department import department_info, department_langues, department_miashs, department_reseaux
from test_course_type import group_type1, group_type2, group_type3, group_type4


@pytest.fixture
def training_l1_info(db, department_info: Department) -> TrainingProgramme:
    return TrainingProgramme.objects.create(
        abbrev="L1INF", name="L1 INFO",
        department=department_info)

@pytest.fixture
def training_l3_langues(db, department_langues: Department) -> TrainingProgramme:
    return TrainingProgramme.objects.create(
        abbrev="L3LNG", name="L3 LANGUES",
        department=department_langues)

@pytest.fixture
def training_m1_reseaux(db, department_reseaux: Department) -> TrainingProgramme:
    return TrainingProgramme.objects.create(
        abbrev="M1RES", name="M1 RESEAUX",
        department=department_reseaux)

@pytest.fixture
def group1(db, group_type1 : GroupType, training_l1_info : TrainingProgramme) -> GenericGroup:
    return GenericGroup.objects.create(
        name = "Group 1",
        train_prog = training_l1_info,
        type = group_type1, size = 1
    )

@pytest.fixture
def group2(db, group_type2 : GroupType, training_l2_miashs : TrainingProgramme) -> GenericGroup:
    return GenericGroup.objects.create(
        name = "Group 2",
        train_prog = training_l2_miashs,
        type = group_type2, size = 2
    )

@pytest.fixture
def group3(db, group_type3 : GroupType, training_m1_reseaux : TrainingProgramme) -> GenericGroup:
    return GenericGroup.objects.create(
        name = "Group 3",
        train_prog = training_m1_reseaux,
        type = group_type3, size = 3
    )

@pytest.fixture
def group4(db, group_type4 : GroupType, training_l3_langues : TrainingProgramme) -> GenericGroup:
    return GenericGroup.objects.create(
        name = "Group 4",
        train_prog = training_l3_langues,
        type = group_type4, size = 4
    )

@pytest.fixture
def group5(db, group_type2 : GroupType, training_l3_miashs : TrainingProgramme) -> GenericGroup:
    return GenericGroup.objects.create(
        name = "Group 5",
        train_prog = training_l3_miashs,
        type = group_type2, size = 5
    )

@pytest.fixture
def group6(db, group_type4 : GroupType, training_l3_langues : TrainingProgramme) -> GenericGroup:
    return GenericGroup.objects.create(
        name = "Group 6",
        train_prog = training_l3_langues,
        type = group_type4, size = 6
    )

# Query
def test_filter_dept (client_query, group2 : GenericGroup, group5 : GenericGroup) :
    query = \
    """
        query {
            genericGroups (dept : "MIASHS") {
                edges {
                    node {
                        name
                        trainProg {
                            name
                        }
                        type {
                            name
                        }
                        size
                    }
                }
            }
        }
    """

    res = execute_query(client_query, query, "genericGroups")
    data = get_data(res)
    names = set([group2.name, group2.type.name, group2.train_prog.name, group5.name, group5.type.name, group5.train_prog.name])
    size = set([group2.size, group5.size])
    assert set(data["name"]) == names
    assert set(data["size"]) == size

def test_with_filters (client_query, group4 : GenericGroup, group6 : GenericGroup):
    query = \
    """
        query {
            genericGroups (dept : "LNG", name_Icontains : "4") {
                edges {
                    node {
                        name
                        size
                    }
                }
            }
        }
    """
    res = execute_query(client_query, query, "genericGroups")
    data = get_data(res)
    assert group4.name in data["name"]
    assert group6.name not in data["name"]

# Mutations
def test_mutations (db, client_query, training_l1_info : TrainingProgramme, group_type1 : GroupType, training_l3_langues : TrainingProgramme, group_type4 : GroupType, capsys):
    group_type1_id = to_global_id("GroupType", group_type1.id)
    group_type4_id = to_global_id("GroupType", group_type4.id)
    training_l1_info_id = to_global_id("TrainingProgramme", training_l1_info.id)
    training_l3_langues_id = to_global_id("TrainingProgramme", training_l3_langues.id)

    create = \
    """ 
        mutation {
            createGenericGroup (
                name : "Group 01"
                size : 11
                trainProg : \"""" + training_l1_info_id + \
    """\"       type : \"""" + group_type1_id + \
    """\"       ) {
                    genericGroup {
                        id
                    }
            }
        }
    """

    global_id = execute_mutation(client_query, create, "createGenericGroup", "genericGroup")
    try:
        obj_id = from_global_id(global_id)[1]
        obj = GenericGroup.objects.get(id=obj_id)
        with capsys.disabled():
            print("The object was created successfully")

        update = \
            """ 
            mutation {
                updateGenericGroup (
                    id : \"""" + global_id + \
            """\"   name : "Group 07"
                    size : 77
                    trainProg : \"""" + training_l3_langues_id + \
        """\"       type : \"""" + group_type4_id + \
        """\" ) {
                        genericGroup {
                            id
                        }
                    }
            }
        """

        execute_mutation(client_query, update, "updateGenericGroup", "genericGroup")
        obj_updated = GenericGroup.objects.get(id=obj_id)
        assert obj.name != obj_updated.name
        assert obj.size != obj_updated.size
        assert obj.train_prog.name != obj_updated.train_prog.name
        assert obj.type.name != obj_updated.type.name
        with capsys.disabled():
            print("The object was updated successfully")

        delete = """
        mutation {
            deleteGenericGroup ( 
                id : \"""" + global_id + \
                """\" ) {
                genericGroup {
                    id
                }
            }
            }
        """
        execute_mutation(client_query, delete, "deleteGenericGroup", "genericGroup")
        try:
            obj_deleted = GenericGroup.objects.get(id=obj_id)
            with capsys.disabled():
                print("The object was not deleted")
        except GenericGroup.DoesNotExist:
            with capsys.disabled():
                print("The object was deleted successfully")
    except GenericGroup.DoesNotExist:
        with capsys.disabled():
            print("The object was not created")
        assert False