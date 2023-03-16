from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from graphql_relay import from_global_id, to_global_id

from base.models import Module, TrainingProgramme, Department, Period, Course, CourseType, GenericGroup, GroupType, Week
from people.models import Tutor

from lib import execute_query, get_data, execute_mutation, client_query


@pytest.fixture
def department_miashs(db) -> Department:
    return Department.objects.create(abbrev="MIASHS", name="Maths Info - SHS")

@pytest.fixture
def training_l2_miashs(db, department_miashs: Department) -> TrainingProgramme:
    return TrainingProgramme.objects.create(
        abbrev="L2M", name="L2 MIASHS",
        department=department_miashs)

@pytest.fixture
def training_l3_miashs(db, department_miashs: Department) -> TrainingProgramme:
    return TrainingProgramme.objects.create(
        abbrev="L3M", name="L3 MIASHS",
        department=department_miashs)

@pytest.fixture
def period_1(db, department_miashs: Department)-> Period:
    return Period.objects.create(
        name="P1", department=department_miashs,
        starting_week=4, ending_week=7)

@pytest.fixture
def period_2(db, department_miashs: Department)-> Period:
    return Period.objects.create(
        name="P2", department=department_miashs,
        starting_week=1, ending_week=4)

@pytest.fixture
def tutor_conception(db, department_miashs : Department) -> Tutor:
    res = Tutor.objects.create(username="JD", first_name="John")
    res.save()
    res.departments.add(department_miashs)
    res.save()
    return res

@pytest.fixture
def tutor_algo_prog(db, department_miashs : Department) -> Tutor:
    res = Tutor.objects.create(username="EM", first_name="Elon")
    res.save()
    res.departments.add(department_miashs)
    res.save()
    return res

@pytest.fixture
def module_conception_log(db, 
training_l3_miashs : TrainingProgramme, tutor_conception : Tutor, period_1 : Period) -> Module:
    return Module.objects.create(abbrev="CPTLog", name="Conception logiciel",
    head=tutor_conception, ppn="azertyuiop", 
    train_prog=training_l3_miashs, period=period_1,
    url="https://cptlog.com",
    description="Lorem ipsum dolor sit amet. In atque alias et eveniet provident eos nisi quisquam quo voluptatem tempore sed voluptas veritatis. Est sint tempore et voluptas accusantium qui ipsam fugiat. In similique eius eos debitis inventore sed nesciunt sint!")

@pytest.fixture
def module_algo_prog(db,
training_l2_miashs : TrainingProgramme, tutor_algo_prog : Tutor, period_2 : Period) -> Module:
    return Module.objects.create(abbrev="ALPG", name="Algo et prog",
    head=tutor_algo_prog, ppn="qsdfghjk", 
    train_prog=training_l2_miashs, period=period_2,
    url="https://algoprog.com",
    description="Est itaque obcaecati id aperiam optio cum praesentium vitae id doloribus aliquid? Et amet culpa ut esse harum aut quisquam aliquam et nemo aperiam et illo internos est Quis eaque non expedita dolor. Ut libero dolor est quasi ipsa At voluptatem alias qui distinctio voluptate sit cupiditate itaque ab vero possimus non quidem quis.")

@pytest.fixture
def group_type1 (db, department_miashs : Department) -> GroupType :
    return GroupType.objects.create(
        name = "Groupe Type 1",
        department = department_miashs
    )

@pytest.fixture
def group_type2 (db, department_miashs : Department) -> GroupType :
    return GroupType.objects.create(
        name = "Groupe Type 2",
        department = department_miashs
    )

@pytest.fixture
def course_type1 (db, group_type1 : GroupType, department_miashs : Department) -> CourseType :
    res = CourseType.objects.create(
        name = "Course Type 1",
        department = department_miashs
    )
    res.group_types.add(group_type1)
    res.save()
    return res

@pytest.fixture
def course_type2 (db, group_type2 : GroupType, department_miashs : Department) -> CourseType :
    res = CourseType.objects.create(
        name = "Course Type 2",
        department = department_miashs
    )
    res.group_types.add(group_type2)
    res.save()
    return res

@pytest.fixture
def group1(db, group_type1 : GroupType, training_l3_miashs : TrainingProgramme) -> GenericGroup:
    return GenericGroup.objects.create(
        name = "Group 1",
        train_prog = training_l3_miashs,
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
def week1(db) -> Week:
    return Week.objects.create(nb=1, year=2022)

@pytest.fixture
def week7(db) -> Week:
    return Week.objects.create(nb=7, year=2021)

@pytest.fixture
def course1(db,tutor_algo_prog:Tutor, course_type1:CourseType, module_algo_prog:Module, group1:GenericGroup, week7 : Week) -> Course:
    res= Course.objects.create(
        type = course_type1,
        week = week7,
        module = module_algo_prog
    )
    res.supp_tutor.add(tutor_algo_prog)
    res.groups.add(group1)
    res.save()
    return res

@pytest.fixture
def course2(db,tutor_conception:Tutor, module_conception_log:Module, course_type2:CourseType,  group2:GenericGroup, week1 : Week) -> Course:
    res = Course.objects.create(
        type = course_type2,
        week = week1,
        module = module_conception_log
    )
    res.supp_tutor.add(tutor_conception)
    res.groups.add(group2)
    res.save()
    return res

def test_all_modules(client_query,
                    module_conception_log : Module, 
                    module_algo_prog : Module):
    query = '''
        query {
            modules (dept :\"MIASHS\"){
                edges {
                    node {
                        abbrev
                        head {
                            username
                        }
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "modules")
    data = get_data(res)
    assert module_conception_log.abbrev in data["abbrev"]
    assert module_algo_prog.abbrev in data["abbrev"]
    assert module_conception_log.head.username in data["username"]
    assert module_algo_prog.head.username in data["username"]

def test_modules_with_filters_1(client_query,
                                module_conception_log: Module, module_algo_prog : Module, course1 : Course, course2 : Course):
    query = """
        query {
            modules (dept :\"MIASHS\", week : "{\\"week\\" : 1, \\"year\\" : 2022}") {
                edges {
                    node {
                        name
                    }
                }
            }
        }
    """
    print(query)
    res = execute_query (client_query, query, "modules")
    data = get_data(res)
    assert module_conception_log.name in data["name"]
    assert module_algo_prog.name not in data["name"]

def test_modules_with_filters_2(client_query,
                                module_algo_prog: Module):
    query = '''
        query {
            modules (dept :\"MIASHS\", name_Icontains : \"l\",
            trainProg_Abbrev : \"L2M\") {
                edges {
                    node {
                        url
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "modules")
    data = get_data(res)
    assert module_algo_prog.url in data["url"]

def test_mutations(db, client_query, tutor_algo_prog : Tutor, tutor_conception : Tutor, period_1 : Period, period_2 : Period, training_l2_miashs : TrainingProgramme, training_l3_miashs : TrainingProgramme, capsys):
    tutor_algo_prog_id = to_global_id("Tutor", tutor_algo_prog.id)
    tutor_conception_id = to_global_id("Tutor", tutor_conception.id)
    period_1_id = to_global_id("Period", period_1.id)
    period_2_id = to_global_id("Period", period_2.id)
    training_l2_miashs_id = to_global_id("TrainingProgramme", training_l2_miashs.id)
    training_l3_miashs_id = to_global_id("TrainingProgramme", training_l3_miashs.id)

    create = \
    """ 
        mutation {
            createModule (
                name : "Module 1"
                abbrev : "MDL1"
                head : \"""" + tutor_algo_prog_id + \
    """\"       ppn : "ppn 1"
                trainProg : \"""" + training_l2_miashs_id + \
    """\"       period : \"""" + period_2_id + \
    """\"       url : "http://module_1.com"
                description : "Azertyuiop"
            ) {
                module {
                    id
                }
            }
        }
    """

    global_id = execute_mutation(client_query, create, "createModule", "module")
    try:
        obj_id = from_global_id(global_id)[1]
        obj = Module.objects.get(id=obj_id)

        update = \
    """ 
        mutation {
            updateModule (
                id : \"""" + global_id + \
    """\"       name : "Module 7"
                abbrev : "MDL7"
                head : \"""" + tutor_conception_id + \
    """\"       ppn : "ppn 7"
                trainProg : \"""" + training_l3_miashs_id + \
    """\"       period : \"""" + period_1_id + \
    """\"       url : "http://module_7.com"
                description : "Qsdfghjklm"
            ) {
                module {
                    id
                }
            }
        }
    """
        execute_mutation(client_query, update, "updateModule", "module")
        obj_updated = Module.objects.get(id=obj_id)
        assert obj.name != obj_updated.name
        assert obj.abbrev != obj_updated.abbrev
        assert obj.head.username != obj_updated.head.username
        assert obj.ppn != obj_updated.ppn
        assert obj.train_prog.name != obj_updated.train_prog.name
        assert obj.period.name != obj_updated.period.name
        assert obj.url != obj_updated.url
        assert obj.description != obj_updated.description
        with capsys.disabled():
            print("The object was updated successfully")
        
        delete = """
        mutation {
            deleteModule ( 
                id : \"""" + global_id + \
                """\" ) {
                module {
                    id
                }
            }
        }
        """

        execute_mutation(client_query, delete, "deleteModule", "module")

        try:
            obj_deleted = Module.objects.get(id=obj_id)
            with capsys.disabled():
                print("The object was not deleted")
        except Module.DoesNotExist:
            with capsys.disabled():
                print("The object was deleted successfully")
    
    except Module.DoesNotExist:
        with capsys.disabled():
            print("The object was not created")
        assert False