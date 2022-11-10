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
    return Course.objects.create( name="Algo")

@pytest.fixture
def scheduled1(db, tutor_conception:Tutor,
                room_algo:Room,
                course_algo:Course) -> ScheduledCourse:
    return ScheduledCourse.objects.create(tutor= tutor_conception, room= room_algo, course= course_algo)



def test_scheduled_course(client_query,
                        scheduled1 : ScheduledCourse):
    query = '''
        query {
            courses {
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
    res = lib.execute_query (client_query, query, "courses")
    data = lib.get_data(res)
    assert scheduled1.tutor.username in data["username"]
    assert scheduled1.room.name in data["name"]
    assert scheduled1.course_types.name in data["name"]


    