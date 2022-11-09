import json
from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
import lib
from people.models import Tutor
from base.models import Course,Room, ScheduledCourse

@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs,
                             client=client,
                             graphql_url="/graphql")

    return func

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
def course_algo(db) -> Course:
    return Course.objects.create( type_name="Algo")

@pytest.fixture
def scheduled1(db, tutor_conception:Tutor,
                room_algo:Room,
                course_algo:Course) -> ScheduledCourse:
    return ScheduledCourse.objects.create(tutor= tutor_conception, room= room_algo, course= course_algo)


def test_scheduled_course(client_query,
                                 tutor_conception: Tutor, 
                    tutor_algo_prog : Tutor, room_algo:Room, course_algo:Course):
    query = '''
        query {
            courses {
                edges {
                    node {
                        tutor{
                            username
                            firstName
                        room{
                            name
                        }
                        }
                    }
                }
            }
        }
    '''
    res = lib.execute_query (client_query, query, "courses")
    data = lib.get_data(res)
    assert tutor_conception_log.first_name in data["firstName"]
    assert tutor_algo_prog.first_name in data["firsName"]
    assert tutor_conception_log.head.username in data["username"]
    assert tutor_algo_prog.head.username in data["username"]
    assert room_algo.name in data["name"]


    