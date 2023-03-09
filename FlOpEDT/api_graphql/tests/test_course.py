from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from base.models import Course, CourseType, Module, Week, RoomType, GenericGroup, TrainingProgramme, Department, Period
from people.models import Tutor
from test_course_type import course_type1, course_type2, course_type3, course_type4, group_type1, group_type2, group_type3, group_type4
from test_modules import module_conception_log, module_algo_prog, period_2, department_miashs
from test_tutor import department_info, tutor_info, tutor_reseaux, department_reseaux
from test_generic_group import group1, group2, group3, group4
from lib import execute_query, get_data, execute_mutation, client_query
from graphql_relay import from_global_id, to_global_id

@pytest.fixture
def training_l2_reseaux(db, department_reseaux: Department) -> TrainingProgramme:
    return TrainingProgramme.objects.create(
        abbrev="L2R", name="L2 RESEAUX",
        department=department_reseaux)


@pytest.fixture
def module_reseaux(db,
training_l2_reseaux: TrainingProgramme, tutor_reseaux : Tutor, period_2 : Period) -> Module:
    return Module.objects.create(abbrev="Res", name="Reseaux",
    head=tutor_reseaux, ppn="qsdfghjk", 
    train_prog=training_l2_reseaux, period=period_2,
    url="https://reseaux.com",
    description="Est itaque obcaecati id aperiam optio cum praesentium vitae id doloribus aliquid? Et amet culpa ut esse harum aut quisquam aliquam et nemo aperiam et illo internos est Quis eaque non expedita dolor. Ut libero dolor est quasi ipsa At voluptatem alias qui distinctio voluptate sit cupiditate itaque ab vero possimus non quidem quis.")


@pytest.fixture
def course1(db,tutor_info:Tutor, course_type1:CourseType, module_algo_prog:Module, group3:GenericGroup) -> Course:
    res= GenericGroup.objects.create(
        name = "group 1",
        type = course_type1,
        module = module_algo_prog
    )
    res.supp_tutor.add(tutor_info)
    res.groups.add(group3)
    res.save()
    return res

@pytest.fixture
def course2(db,tutor_reseaux:Tutor, module_conception_log:Module, course_type2:CourseType,  group1:GenericGroup) -> Course:
    res = GenericGroup.objects.create(
        name = "group 2",
        type = course_type2,
      
        module = module_conception_log
    )
    res.supp_tutor.add(tutor_reseaux)
    res.groups.add(group1)
    res.save()
    return res

@pytest.fixture
def course3(db, tutor_reseaux:Tutor, module_reseaux:Module, course_type4:CourseType, group2:GenericGroup) -> Course:
    res = GenericGroup.objects.create(
        name = "group 3",
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
            courses(dept: "RT"){
                edges{
                    node{
                        name
                    
                    }
            }
            }
        }
    """
    res = execute_query(client_query, query, "Course")
    data = get_data(res)
    names = set([course1.name, course2.name, course3.name])
    assert set(data["names"])==names



