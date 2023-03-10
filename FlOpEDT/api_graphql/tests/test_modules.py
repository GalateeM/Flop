from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from base.models import Module, TrainingProgramme, Department, Period
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
                                module_conception_log: Module):
    query = '''
        query {
            modules (dept :\"MIASHS\", week : 5) {
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
    assert module_conception_log.url in data["url"]

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

# def test_mutations(db, client_query, tutor_algo_prog : Tutor, tutor_conception : Tutor, period_1 : Period, period_2 : Period, training_l2_miashs : TrainingProgramme, training_l3_miashs : TrainingProgramme, capsys):
#     #tutor
#     #Train_prog
#     #period
#     tutor_algo_prog_id = to_global_id("Tutor", tutor_algo_prog.id)
#     tutor_conception_id = to_global_id("Tutor", tutor_conception.id)
#     period_1_id = to_global_id("Period", period_1.id)
#     period_2_id = to_global_id("Period", period_2.id)
#     training_l2_miashs_id = to_global_id("TrainingProgramme", training_l2_miashs)
#     training_l3_miashs_id = to_global_id("TrainingProgramme", training_l3_miashs)

#     create = \
#     """ 
#         mutation {
#             createModule (
#                 name : "Module 1"
#                 abbrev : "MDL1"
#                 head : \"""" + tutor_algo_prog_id + \
#     """\"       ppn : "ppn 1"
#                 train_prog : \"""" + training_l2_miashs_id + \
#     """\"       period : \"""" + period_2_id + \
#     """\"       url : "http://module_1.com"
#                 description : "Azertyuiop"
#             ) {
#                 module {
#                     id
#                 }
#             }
#         }
#     """

#     global_id = execute_mutation(client_query, create, "createModule", "module")
#     try:
#         obj_id = from_global_id(global_id)[1]
#         obj = Module.objects.get(id=obj_id)

#         update = \
#     """ 
#         mutation {
#             updateModule (
#                 name : "Module 7"
#                 abbrev : "MDL7"
#                 head : \"""" + tutor_conception_id + \
#     """\"       ppn : "ppn 7"
#                 train_prog : \"""" + training_l3_miashs_id + \
#     """\"       period : \"""" + period_1_id + \
#     """\"       url : "http://module_7.com"
#                 description : "Qsdfghjklm"
#             ) {
#                 module {
#                     id
#                 }
#             }
#         }
#     """
#         execute_mutation(client_query, update, "updateModule", "module")
#         obj_updated = Module.objects.get(id=obj_id)
#         assert obj.name != obj_updated.name
#         assert obj.abbrev != obj_updated.abbrev
#         assert obj.head.username != obj_updated.head.username
#         assert obj.ppn != obj_updated.ppn
#         assert obj.train_prog.name != obj_updated.train_prog.name
#         assert obj.period.name != obj_updated.period.name
#         assert obj.url != obj_updated.url
#         assert obj.description != obj_updated.description
#         with capsys.disabled():
#             print("The object was updated successfully")
        
#         delete = """
#         mutation {
#             deleteModule ( 
#                 id : \"""" + global_id + \
#                 """\" ) {
#                 module {
#                     id
#                 }
#             }
#         }
#         """

#         execute_mutation(client_query, delete, "deleteModule", "module")

#         try:
#             obj_deleted = Module.objects.get(id=obj_id)
#             with capsys.disabled():
#                 print("The object was not deleted")
#         except Module.DoesNotExist:
#             with capsys.disabled():
#                 print("The object was deleted successfully")
    
#     except Module.DoesNotExist:
#         with capsys.disabled():
#             print("The object was not created")
#         assert False