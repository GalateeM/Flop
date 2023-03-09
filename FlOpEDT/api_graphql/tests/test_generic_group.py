from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from base.models import TrainingProgramme, Department, GroupType, GenericGroup
from test_modules import training_l2_miashs, training_l3_miashs
from test_department import department_info, department_langues, department_miashs, department_reseaux
from test_course_type import group_type1, group_type2, group_type3, group_type4
from lib import execute_query, get_data, execute_mutation, client_query
from graphql_relay import from_global_id, to_global_id

# Train_prog
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

# Group types
#1 info 2 misahs 3 reseaux 4 langues

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