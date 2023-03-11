from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from graphql_relay import from_global_id, to_global_id

from base.models import Course, CourseType, Module, GenericGroup, TrainingProgramme, Department, Period
from people.models import Tutor

from lib import execute_query, get_data, execute_mutation, client_query
from test_tutor import department_info, department_miashs, department_reseaux, tutor_reseaux, tutor_info, tutor_algo_prog, tutor_conception
from test_course_type import course_type1, course_type2, course_type4
from test_modules import training_l2_miashs, training_l3_miashs, period_1, period_2, module_algo_prog, module_conception_log
from test_generic_group import group_type1, group_type2, group_type3, training_m1_reseaux, training_l1_info, group3, group1, group2, group4, group_type4, department_langues, training_l3_langues


@pytest.fixture
def training_l2_reseaux(db, department_reseaux: Department) -> TrainingProgramme:
    return TrainingProgramme.objects.create(
        abbrev="L2R", name="L2 RESEAUX",
        department=department_reseaux)

@pytest.fixture
def module_reseaux(db, training_l2_reseaux: TrainingProgramme, tutor_reseaux : Tutor, period_2 : Period) -> Module:
    return Module.objects.create(abbrev="RES", name="Reseaux",
    head=tutor_reseaux, ppn="qsdfghjk", 
    train_prog=training_l2_reseaux, period=period_2,
    url="https://reseaux.com",
    description="Est itaque obcaecati id aperiam optio cum praesentium vitae id doloribus aliquid? Et amet culpa ut esse harum aut quisquam aliquam et nemo aperiam et illo internos est Quis eaque non expedita dolor. Ut libero dolor est quasi ipsa At voluptatem alias qui distinctio voluptate sit cupiditate itaque ab vero possimus non quidem quis.")


@pytest.fixture
def course1(db,tutor_info:Tutor, course_type1:CourseType, module_algo_prog:Module, group3:GenericGroup) -> Course:
    res= Course.objects.create(
        type = course_type1,
        module = module_algo_prog
    )
    res.supp_tutor.add(tutor_info)
    res.groups.add(group3)
    res.save()
    return res

@pytest.fixture
def course2(db,tutor_conception:Tutor, module_conception_log:Module, course_type2:CourseType,  group1:GenericGroup) -> Course:
    res = Course.objects.create(
        type = course_type2,
        module = module_conception_log
    )
    res.supp_tutor.add(tutor_conception)
    res.groups.add(group1)
    res.save()
    return res

@pytest.fixture
def course3(db, tutor_reseaux:Tutor, module_reseaux:Module, course_type4:CourseType, group2:GenericGroup) -> Course:
    res = Course.objects.create(
        type = course_type4,
        module = module_reseaux
    )
    res.supp_tutor.add(tutor_reseaux)
    res.groups.add(group2)
    res.save()
    return res

"""Test Query"""
def test_no_filter(client_query, course1:Course, course2:Course, course3:Course):
    query = \
    """
        query{
            courses(dept: "MIASHS"){
                edges{
                    node{
                        type {
                            name
                        }
                        module {
                            name
                        }
                        suppTutor {
                            edges {
                                node {
                                    username
                                }
                            }
                        }
                    }
            }
            }
        }
    """
    res = execute_query(client_query, query, "courses")
    data = get_data(res)
    name = set([course1.type.name, course1.module.name, course2.type.name, course2.module.name])
    assert name == set(data["name"])
    assert course3.type.name not in data["name"]
    assert course3.module.name not in data["name"]
    for tutor in course1.supp_tutor.all():
        assert tutor.username in data["username"]
    for tutor in course2.supp_tutor.all():
        assert tutor.username in data["username"]
    for tutor in course3.supp_tutor.all():
        assert tutor.username not in data["username"]

def test_filters(client_query, course1:Course, course2:Course):
    query = \
    """
        query{
            courses(dept: "MIASHS", type_Name_Icontains : "1"){
                edges{
                    node{
                        type {
                            name
                        }
                    }
            }
            }
        }
    """
    res = execute_query(client_query, query, "courses")
    data = get_data(res)
    assert course1.type.name in data["name"]
    assert course2.type.name not in data["name"]

# Mutations
def test_mutations (db, client_query, course_type1 : CourseType, course_type2 : CourseType, module_algo_prog : Module, module_conception_log : Module, group3 : GenericGroup, group1 : GenericGroup, group2 : GenericGroup, group4 : GenericGroup, tutor_reseaux : Tutor, tutor_info : Tutor, tutor_algo_prog : Tutor, tutor_conception : Tutor, capsys) :
    course_type1_id = to_global_id("CourseType", course_type1.id)
    course_type2_id = to_global_id("CourseType", course_type2.id)    
    module_algo_prog_id = to_global_id("Module", module_algo_prog.id)
    module_conception_log_id = to_global_id("Module", module_conception_log.id)
    group_1_id = to_global_id("GenericGroup", group1.id)
    group_2_id = to_global_id("GenericGroup", group2.id)
    group_3_id = to_global_id("GenericGroup", group3.id)
    group_4_id = to_global_id("GenericGroup", group4.id)
    tutor_reseaux_id = to_global_id("Tutor", tutor_reseaux.id)
    tutor_algo_prog_id = to_global_id("Tutor", tutor_algo_prog.id)
    tutor_conception_id = to_global_id("Tutor", tutor_conception.id)
    tutor_info_id = to_global_id("Tutor", tutor_info.id) 
    
    create = \
    """
        mutation {
            createCourse (
                type : \"""" + course_type1_id + \
    """\"       module : \"""" + module_algo_prog_id + \
    """\"       groups : [\"""" + group_1_id + "\", \"" + group_2_id + \
    """\"]      suppTutor : [\"""" + tutor_algo_prog_id + """\", \"""" + tutor_conception_id + \
    """\"]      
        ) {
            courses {
                id
            }
        }
    }
    """

    global_id = execute_mutation(client_query, create, "createCourse", "courses")
    try:
        obj_id = from_global_id(global_id)[1]
        obj = Course.objects.get(id=obj_id)
        groups_obj = tutors_obj = []
        for g in obj.groups.all():
            groups_obj.append(g.name)
        for t in obj.supp_tutor.all():
            tutors_obj.append(t.username)

        with capsys.disabled():
            print("The object was created successfully")
        update = \
        """
        mutation {
            updateCourse (
                id : \"""" + global_id + \
    """\"       type : \"""" + course_type2_id + \
    """\"       module : \"""" + module_conception_log_id + \
    """\"       groups : [\"""" + group_3_id + "\", \"" + group_4_id + \
    """\"]      suppTutor : [\"""" + tutor_info_id + """\", \"""" + tutor_reseaux_id + \
    """\"]      
        ) {
            courses {
                id
            }
        }
    }
    """

        execute_mutation(client_query, update, "updateCourse", "courses")
        obj_updated = Course.objects.get(id=obj_id)
        assert obj.type.name != obj_updated.type.name
        assert obj.module.name != obj_updated.module.name
        groups_obj_updated = tutors_obj_updated = []
        for g in obj_updated.groups.all():
            groups_obj_updated.append(g.name)
        for t in obj_updated.supp_tutor.all():
            tutors_obj_updated.append(t.username)
        assert set(groups_obj) != set(groups_obj_updated)
        assert set(tutors_obj) != set(tutors_obj_updated)
        with capsys.disabled():
            print("The object was updated successfully")

        delete = """
        mutation {
            deleteCourse ( 
                id : \"""" + global_id + \
                """\" ) {
                courses {
                    id
                }
            }
            }
        """
        execute_mutation(client_query, delete, "deleteCourse", "courses")
        try:
            obj_deleted = Course.objects.get(id=obj_id)
            with capsys.disabled():
                print("The object was not deleted")
        except Course.DoesNotExist:
            with capsys.disabled():
                print("The object was deleted successfully")

    except Course.DoesNotExist:
        with capsys.disabled():
            print("The object was not created")
        assert False