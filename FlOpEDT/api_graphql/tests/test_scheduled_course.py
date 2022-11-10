import json
from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
import lib
from people.models import Tutor
from base.models import Course,Room, ScheduledCourse, CourseType, Module, TrainingProgramme, Department, Period
from test_modules import department_miashs

@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs,
                             client=client,
                             graphql_url="/graphql")

    return func




@pytest.fixture
def training_l2_miashs(db, department_miashs: Department) -> TrainingProgramme:
    return TrainingProgramme.objects.create(
        abbrev="L2M", name="L2 MIASHS",
        department=department_miashs)

@pytest.fixture
def tutor_algo_prog(db) -> Tutor:
    return Tutor.objects.create(username="EM", first_name="Elon")

@pytest.fixture
def period_2(db, department_miashs: Department)-> Period:
    return Period.objects.create(
        name="P2", department=department_miashs,
        starting_week=1, ending_week=4)

@pytest.fixture
def module_algo_prog(db,
training_l2_miashs : TrainingProgramme, tutor_algo_prog : Tutor, period_2 : Period) -> Module:
    return Module.objects.create(abbrev="ALPG", name="Algo et prog",
    head=tutor_algo_prog, ppn="qsdfghjk", 
    train_prog=training_l2_miashs, period=period_2,
    url="https://algoprog.com",
    description="Est itaque obcaecati id aperiam optio cum praesentium vitae id doloribus aliquid? Et amet culpa ut esse harum aut quisquam aliquam et nemo aperiam et illo internos est Quis eaque non expedita dolor. Ut libero dolor est quasi ipsa At voluptatem alias qui distinctio voluptate sit cupiditate itaque ab vero possimus non quidem quis.")





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
def course_algo(db, course_type_algo:CourseType,
module_algo_prog:Module) -> Course:
    return Course.objects.create( type= course_type_algo, module=module_algo_prog)


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
    res = lib.execute_query (client_query, query, "scheduledCourses")
    data = lib.get_data(res)
    assert scheduled1.tutor.username in data["username"]
    assert scheduled1.room.name in data["name"]
    assert scheduled1.course.type.name in data["name"]


    
