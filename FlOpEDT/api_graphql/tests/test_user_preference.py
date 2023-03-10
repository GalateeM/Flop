from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from base.models import UserPreference, Week
from people.models import Tutor
from base.timing import Day
from base.models import Week, Course,Room, ScheduledCourse, CourseType, Module, TrainingProgramme, Department, Period
from test_modules import department_miashs, tutor_algo_prog, tutor_conception
from lib import execute_query, get_data, execute_mutation, client_query
from graphql_relay import from_global_id, to_global_id

@pytest.fixture
def week1(db) -> Week:
    return Week.objects.create(nb=1, year=2022)

@pytest.fixture
def week7(db) -> Week:
    return Week.objects.create(nb=7, year=2021)

@pytest.fixture
def user_pref_algo_prog(db, \
    tutor_algo_prog : Tutor, week7 : Week) -> UserPreference:
    return UserPreference.objects.create(
        user = tutor_algo_prog,week = week7,
        start_time = 2, duration = 3,
        day = Day.THURSDAY, value = 5 
    )

@pytest.fixture
def user_pref_conception(db, \
    tutor_conception : Tutor, week1 : Week) -> UserPreference:
    return UserPreference.objects.create(
        user = tutor_conception,week = week1,
        start_time = 1, duration = 1,
        day = Day.FRIDAY, value = 2 
    )

@pytest.fixture
def user_pref_conception2(db, \
    tutor_algo_prog : Tutor, week1 : Week) -> UserPreference:
    return UserPreference.objects.create(
        user = tutor_algo_prog,week = week1,
        start_time = 1, duration = 1,
        day = Day.FRIDAY, value = 2 
    )

# Query

def test_filter_week_year(client_query, user_pref_algo_prog : UserPreference, user_pref_conception : UserPreference, user_pref_conception2 : UserPreference):
    query = '''
        query {
            userPreferences (week : 7, year : 2021) {
                edges {
                    node {
                        week {
                            year
                        }
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "userPreferences")
    data = get_data(res)
    assert user_pref_algo_prog.week.year in data["year"]
    assert user_pref_conception.week.year not in data["year"]
    assert user_pref_conception2.week.year not in data["year"]

def test_filters(client_query, user_pref_conception : UserPreference, user_pref_conception2 : UserPreference):
    query = '''
        query {
            userPreferences (dept : \"MIASHS\", week : 1, year : 2022, user_Username : "JD") {
                edges {
                    node {
                        user {
                            username
                        }
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "userPreferences")
    data = get_data(res)
    assert user_pref_conception.user.username in data["username"]
    assert user_pref_conception2.user.username not in data["username"]

# Mutation

def test_mutations(db, client_query, tutor_algo_prog : Tutor, tutor_conception : Tutor, week1 : Week, week7 : Week, capsys):
    tutor_algo_prog_id = to_global_id("Tutor", tutor_algo_prog.id)
    tutor_conception_id = to_global_id("Tutor", tutor_conception.id)
    week1_id = to_global_id("Week", week1.id)
    week7_id = to_global_id("Week", week7.id)

    create = \
    """
        mutation {
            createUserPreference (
                week : \"""" + week7_id + \
    """\"       user : \"""" + tutor_algo_prog_id + \
    """\"       startTime : 2
                duration : 1,
                day : "f"
                value : 4
            ) {
                userPreference {
                    id
                }
            }
        }
    """

    global_id = execute_mutation(client_query, create, "createUserPreference", "userPreference")
    try:
        obj_id = from_global_id(global_id)[1]
        obj = UserPreference.objects.get(id=obj_id)
        with capsys.disabled():
            print("The object was created successfully")

        update = \
        """
                mutation {
                    updateUserPreference (
                    id : \"""" + global_id + \
        """\"
                    week : \"""" + week1_id + \
        """\"       user : \"""" + tutor_conception_id + \
        """\"       startTime : 1
                    duration : 2,
                    day : "m"
                    value : 3
                ) {
                userPreference {
                    id
                }
            }
            }
        """

        execute_mutation(client_query, update, "updateUserPreference", "userPreference")
        obj_updated = UserPreference.objects.get(id=obj_id)
        assert obj.week.nb != obj_updated.week.nb
        assert obj.week.year != obj_updated.week.year        
        assert obj.start_time != obj_updated.start_time
        assert obj.user.username != obj_updated.user.username
        assert obj.duration != obj_updated.duration
        assert obj.day != obj_updated.day

        with capsys.disabled():
            print("The object was updated successfully")

        delete = """
        mutation {
            deleteUserPreference ( 
                id : \"""" + global_id + \
                """\" ) {
                userPreference {
                    id
                }
            }
            }
        """
        execute_mutation(client_query, delete, "deleteUserPreference", "userPreference")
        try:
            obj_deleted = UserPreference.objects.get(id=obj_id)
            with capsys.disabled():
                print("The object was not deleted")
        except UserPreference.DoesNotExist:
            with capsys.disabled():
                print("The object was deleted successfully")

    except UserPreference.DoesNotExist:
        with capsys.disabled():
            print("The object was not created")
        assert False
