from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from people.models import Tutor
from base.models import Week, Course,Room, ScheduledCourse, CourseType, Module, TrainingProgramme, Department, Period
from test_modules import module_algo_prog, module_conception_log, training_l3_miashs ,training_l2_miashs, \
department_miashs, period_1 , period_2, tutor_algo_prog, tutor_conception
from test_user_preference import week1, week7
from lib import execute_query, get_data, execute_mutation, client_query
from graphql_relay import from_global_id, to_global_id

@pytest.fixture
def course_type_algo(db) -> CourseType:
    return CourseType.objects.create(name= "Algo")

@pytest.fixture
def room_algo(db) -> Room:
    return Room.objects.create( name="B101")

@pytest.fixture
def course_algo(db, module_algo_prog: Module, course_type_algo: CourseType, week7 : Week) -> Course:
    return Course.objects.create(module=module_algo_prog, type= course_type_algo, week = week7)


@pytest.fixture
def scheduled1(db, tutor_algo_prog:Tutor,
                room_algo:Room,
                course_algo:Course) -> ScheduledCourse:
    return ScheduledCourse.objects.create(tutor= tutor_algo_prog, room= room_algo, course= course_algo, start_time = 5)

@pytest.fixture
def course_type_conception(db) -> CourseType:
    return CourseType.objects.create(name= "Conception") 

@pytest.fixture
def room_algo(db) -> Room:
    return Room.objects.create( name="B101")

@pytest.fixture
def room_conception(db) -> Room:
    return Room.objects.create( name="Z909")

@pytest.fixture
def course_conception(db, module_conception_log: Module, course_type_conception:CourseType, week1 : Week) -> Course:
    return Course.objects.create(module=module_conception_log, type= course_type_conception, week = week1)

@pytest.fixture
def scheduled2(db, tutor_conception:Tutor,
                room_conception:Room,
                course_conception:Course) -> ScheduledCourse:
    return ScheduledCourse.objects.create(tutor= tutor_conception, room= room_conception, course= course_conception, start_time = 2)

@pytest.fixture
def scheduled2(db, tutor_conception:Tutor,
                room_conception:Room,
                course_conception:Course) -> ScheduledCourse:
    return ScheduledCourse.objects.create(tutor= tutor_conception, room= room_conception, course= course_conception, start_time = 2)

@pytest.fixture
def scheduled3(db, tutor_algo_prog:Tutor,
                room_conception:Room,
                course_conception:Course) -> ScheduledCourse:
    return ScheduledCourse.objects.create(tutor= tutor_algo_prog, room= room_conception, course= course_conception, start_time = 2)

# Query

def test_filter_week_year(client_query,
                        scheduled1 : ScheduledCourse, scheduled2 : ScheduledCourse):
    query = '''
        query {
            scheduledCourses (week: 7, year : 2021) {
                edges {
                    node {
                        tutor{
                            username
                        }   
                        room{
                            name
                        }
                        course{
                            type {
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
    assert scheduled2.tutor.username not in data["username"]
    assert scheduled2.room.name not in data["name"]
    assert scheduled2.course.type.name not in data["name"]

def test_filters(client_query,
                        scheduled2 : ScheduledCourse, scheduled3 : ScheduledCourse):
    query = '''
        query {
            scheduledCourses (week: 1, year : 2022, tutor_Username_Icontains : "JD") {
                edges {
                    node {
                        tutor{
                            username
                        }   
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "scheduledCourses")
    data = get_data(res)
    assert scheduled2.tutor.username in data["username"]
    assert scheduled3.tutor.username not in data["username"]

# Mutations
def test_mutations(db, client_query, course_conception : Course, course_algo : Course, room_algo : Room, room_conception : Room, tutor_algo_prog : Tutor, tutor_conception : Tutor, capsys):
    course_conception_id = to_global_id("Course", course_conception.id)
    course_algo_id = to_global_id("Course", course_algo.id)
    room_algo_id = to_global_id("Room", room_algo.id)
    room_conception_id = to_global_id("Room", room_conception.id)
    tutor_algo_prog_id = to_global_id("Course", tutor_algo_prog.id) 
    tutor_conception_id = to_global_id("Course", tutor_conception.id)

    create = \
    """
        mutation {
            createScheduledCourse (
                course : \"""" + course_conception_id + \
    """\"       room : \"""" + room_conception_id + \
    """\"       tutor : \"""" + tutor_conception_id + \
    """\"       startTime : 2
            ) {
                scheduledCourses {
                    id
                }
            }
        }
    """
    global_id = execute_mutation(client_query, create, "createScheduledCourse", "scheduledCourses")
    try:
        obj_id = from_global_id(global_id)[1]
        obj = ScheduledCourse.objects.get(id=obj_id)

        with capsys.disabled():
            print("The object was created successfully")
        
        update = \
        """
            mutation {
                updateScheduledCourse (
                    id : \"""" + global_id + \
        """\"       course : \"""" + course_algo_id + \
        """\"       room : \"""" + room_algo_id + \
        """\"       tutor : \"""" + tutor_algo_prog_id + \
        """\"       startTime : 5
                ) {
                    scheduledCourses {
                        id
                    }
                }
            }
        """

        execute_mutation(client_query, update, "updateScheduledCourse", "scheduledCourses")
        obj_updated = ScheduledCourse.objects.get(id=obj_id)
        assert obj.course.week.nb != obj_updated.course.week.nb
        assert obj.course.week.year != obj_updated.course.week.year
        assert obj.room.name != obj_updated.room.name
        assert obj.tutor.username != obj_updated.tutor.username
        with capsys.disabled():
            print("The object was updated successfully")

        delete = """
        mutation {
            deleteScheduledCourse ( 
                id : \"""" + global_id + \
                """\" ) {
                scheduledCourses {
                    id
                }
            }
            }
        """
        execute_mutation(client_query, delete, "deleteScheduledCourse", "scheduledCourses")
        try:
            obj_deleted = ScheduledCourse.objects.get(id=obj_id)
            with capsys.disabled():
                print("The object was not deleted")
        except ScheduledCourse.DoesNotExist:
            with capsys.disabled():
                print("The object was deleted successfully")

    except ScheduledCourse.DoesNotExist:
        with capsys.disabled():
            print("The object was not created")
        assert False