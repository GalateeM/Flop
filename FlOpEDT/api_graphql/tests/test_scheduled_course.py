from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from people.models import Tutor
from base.models import Course,Room, ScheduledCourse, CourseType, Module, TrainingProgramme, Department, Period
from test_modules import module_algo_prog, training_l2_miashs, department_miashs, period_2
from lib import *

@pytest.fixture
def course_type_algo(db) -> CourseType:
    return CourseType.objects.create(name= "Algo")

@pytest.fixture
def tutor_conception(db) -> Tutor:
    return Tutor.objects.create(username="JD", first_name="John")

@pytest.fixture
def tutor_algo_prog(db) -> Tutor:
    return Tutor.objects.create(username="EM", first_name="Elon")
 

@pytest.fixture
def room_algo(db) -> Room:
    return Room.objects.create( name="B101")

@pytest.fixture
def course_algo(db, module_algo_prog: Module, course_type_algo:CourseType) -> Course:
    return Course.objects.create(module=module_algo_prog, type= course_type_algo)


@pytest.fixture
def scheduled1(db, tutor_conception:Tutor,
                room_algo:Room,
                course_algo:Course) -> ScheduledCourse:
    return ScheduledCourse.objects.create(tutor= tutor_conception, room= room_algo, course= course_algo, start_time = 5)



def test_scheduled_course(client_query,
                        scheduled1 : ScheduledCourse):
    query = '''
        query {
            scheduledCourses {
                edges {
                    node {
                        tutor{
                            username
                        }   
                        room{
                            name
                        }
                        course{
                            type{
                                name
                            }
                        }
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "scheduledCourses")
    data = get_data(res)
    assert scheduled1.tutor.username in data["username"]
    assert scheduled1.room.name in data["name"]
    assert scheduled1.course.type.name in data["name"]


    
