# from _pytest.fixtures import fixture
# import pytest
# from graphene_django.utils.testing import graphql_query

# from base.models import Course, ScheduledCourse, TrainingProgramme, Department, Period \
# , Module, GroupType, CourseType, GenericGroup, Room, Week
# from people.models import Tutor

# from lib import execute_query, get_data, execute_mutation, client_query
# from test_department import department_info, department_langues

# @pytest.fixture
# def training1_info(db, department_info: Department) -> TrainingProgramme:
#     return TrainingProgramme.objects.create(
#         abbrev="TR1INF", name="TRN 1 INFO",
#         department=department_info)

# @pytest.fixture
# def training2_info(db, department_info: Department) -> TrainingProgramme:
#     return TrainingProgramme.objects.create(
#         abbrev="TR2INF", name="TRN 2 INFO",
#         department=department_info)

# @pytest.fixture
# def training_langues(db, department_langues: Department) -> TrainingProgramme:
#     return TrainingProgramme.objects.create(
#         abbrev="TRLNG", name="TRN LANGUES",
#         department=department_langues)

# @pytest.fixture
# def period1_info(db, department_info: Department)-> Period:
#     return Period.objects.create(
#         name="P1INF", department=department_info,
#         starting_week=1, ending_week=7)

# @pytest.fixture
# def period2_info(db, department_info: Department)-> Period:
#     return Period.objects.create(
#         name="P2INF", department=department_info,
#         starting_week=8, ending_week=14)

# @pytest.fixture
# def period_langues(db, department_langues: Department)-> Period:
#     return Period.objects.create(
#         name="PLNG", department=department_langues,
#         starting_week=4, ending_week=11)

# @pytest.fixture
# def tutor1_info(db, department_info : Department) -> Tutor:
#     res = Tutor.objects.create(username="TI1", first_name="Tutor 1 Info", last_name = "Lst1")
#     res.save()
#     res.departments.add(department_info)
#     res.save()
#     return res

# @pytest.fixture
# def tutor2_info(db, department_info : Department) -> Tutor:
#     res = Tutor.objects.create(username="TI2", first_name="Tutor 2 Info", last_name = "Lst2")
#     res.save()
#     res.departments.add(department_info)
#     res.save()
#     return res

# @pytest.fixture
# def tutor_langues(db, department_langues : Department) -> Tutor:
#     res = Tutor.objects.create(username="TLNG", first_name="Tutor Langues", last_name = "LstLng")
#     res.save()
#     res.departments.add(department_langues)
#     res.save()
#     return res

# @pytest.fixture
# def module1_info(db, 
# training1_info : TrainingProgramme, tutor1_info : Tutor, period1_info : Period) -> Module:
#     return Module.objects.create(abbrev="MDL1INF", name="Module 1 Info",
#     head=tutor1_info, 
#     train_prog=training1_info, period=period1_info)

# @pytest.fixture
# def module2_info(db, 
# training2_info : TrainingProgramme, tutor2_info : Tutor, period2_info : Period) -> Module:
#     return Module.objects.create(abbrev="MDL2INF", name="Module 2 Info",
#     head=tutor2_info, 
#     train_prog=training2_info, period=period2_info)

# @pytest.fixture
# def module_langues(db, 
# training_langues : TrainingProgramme, tutor_langues : Tutor, period_langues : Period) -> Module:
#     return Module.objects.create(abbrev="MDLNG", name="Module Langues",
#     head=tutor_langues, 
#     train_prog=training_langues, period=period_langues)

# @pytest.fixture
# def group_type_info (db, department_info : Department) -> GroupType :
#     return GroupType.objects.create(
#         name = "Groupe Type Info",
#         department = department_info
#     )

# @pytest.fixture
# def group_type_langues (db, department_langues : Department) -> GroupType :
#     return GroupType.objects.create(
#         name = "Groupe Type Langues",
#         department = department_langues
#     )

# @pytest.fixture
# def course_type_info (db, group_type_info : GroupType, department_info : Department) -> CourseType :
#     res = CourseType.objects.create(
#         name = "Course Type Info",
#         department = department_info
#     )
#     res.group_types.add(group_type_info)
#     res.save()
#     return res

# @pytest.fixture
# def course_type_langues (db, group_type_langues : GroupType, department_langues : Department) -> CourseType :
#     res = CourseType.objects.create(
#         name = "Course Type Langues",
#         department = department_langues
#     )
#     res.group_types.add(group_type_langues)
#     res.save()
#     return res

# @pytest.fixture
# def group1_info(db, group_type_info : GroupType, training1_info : TrainingProgramme) -> GenericGroup:
#     return GenericGroup.objects.create(
#         name = "Group 1 Info",
#         train_prog = training1_info,
#         type = group_type_info, size = 1
#     )

# @pytest.fixture
# def group2_info(db, group_type_info : GroupType, training2_info : TrainingProgramme) -> GenericGroup:
#     return GenericGroup.objects.create(
#         name = "Group 2 Info",
#         train_prog = training2_info,
#         type = group_type_info, size = 1
#     )

# @pytest.fixture
# def group_langues(db, group_type_langues : GroupType, training_langues : TrainingProgramme) -> GenericGroup:
#     return GenericGroup.objects.create(
#         name = "Group langues",
#         train_prog = training_langues,
#         type = group_type_langues, size = 1
#     )

# @pytest.fixture
# def room1_info(db) -> Room:
#     return Room.objects.create( name="INF101")

# @pytest.fixture
# def week4_info(db) -> Week:
#     return Week.objects.create(nb=4, year=2022)

# @pytest.fixture
# def week2_info(db) -> Week:
#     return Week.objects.create(nb=2, year=2022)

# @pytest.fixture
# def week_langues(db) -> Week:
#     return Week.objects.create(nb=4, year=2022)

# @pytest.fixture
# def course_langues(db,tutor_langues:Tutor, module_langues:Module, course_type_langues:CourseType,  group_langues:GenericGroup, week_langues : Week) -> Course:
#     res = Course.objects.create(
#         type = course_type_langues,
#         module = module_langues, 
#         week = week_langues,
#         no = 0
#     )
#     res.supp_tutor.add(tutor_langues)
#     res.groups.add(group_langues)
#     res.save()
#     return res

# @pytest.fixture
# def course1_info(db,tutor1_info:Tutor, module1_info:Module, course_type_info:CourseType,  group1_info:GenericGroup, week4_info : Week) -> Course:
#     res = Course.objects.create(
#         type = course_type_info,
#         module = module1_info, 
#         week = week4_info,
#         no = 1
#     )
#     res.supp_tutor.add(tutor1_info)
#     res.groups.add(group1_info)
#     res.save()
#     return res

# @pytest.fixture
# def course2_info(db,tutor2_info:Tutor, module2_info:Module, course_type_info:CourseType,  group2_info:GenericGroup, week2_info : Week) -> Course:
#     res = Course.objects.create(
#         type = course_type_info,
#         module = module2_info, 
#         week = week2_info,
#         no = 2
#     )
#     res.supp_tutor.add(tutor2_info)
#     res.groups.add(group2_info)
#     res.save()
#     return res
    
# @pytest.fixture
# def course3_info(db,tutor2_info:Tutor, module2_info:Module, course_type_info:CourseType,  group1_info:GenericGroup, week4_info : Week) -> Course:
#     res = Course.objects.create(
#         type = course_type_info,
#         module = module2_info, 
#         week = week4_info,
#         no = 3
#     )
#     res.supp_tutor.add(tutor2_info)
#     res.groups.add(group1_info)
#     res.save()
#     return res

# @pytest.fixture
# def scheduled3_info(db, tutor1_info:Tutor,
#                 room1_info:Room,
#                 course3_info:Course) -> ScheduledCourse:
#     return ScheduledCourse.objects.create(tutor= tutor1_info, room= room1_info, course= course3_info, start_time = 5, work_copy = 1)

# def test(client_query, course1_info : Course, course2_info : Course, course3_info : Course, scheduled3_info : ScheduledCourse, course_langues : Course):
#     query = \
#     """
#         query {
#             unscheduledCourses (dept : "INFO", year : 2022, week : 4) {
#                 edges {
#                     node {
#                         no                
#                     }
#                 }
#             }
#         }
#     """

#     res = execute_query(client_query, query, "unscheduledCourses")
#     data = get_data(res)
#     assert len(data["no"]) == 1
#     assert course_langues.no not in data["no"]
#     assert course1_info.no in data["no"]
#     assert course2_info.no not in data["no"]
#     assert course3_info.no not in data["no"]