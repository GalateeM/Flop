from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from base.models import CourseType, GroupType , Department
from test_tutor import department_info, department_miashs, department_reseaux
from lib import execute_query, get_data, execute_mutation, client_query
from graphql_relay import from_global_id, to_global_id

@pytest.fixture
def department_langues (db) -> Department :
    return Department.objects.create(
        name = "Langues",
        abbrev = "LNG"
    )

@pytest.fixture
def group_type1 (db, department_info : Department) -> GroupType :
    return GroupType.objects.create(
        name = "Groupe Type 1",
        department = department_info
    )

@pytest.fixture
def group_type2 (db, department_miashs : Department) -> GroupType :
    return GroupType.objects.create(
        name = "Groupe Type 2",
        department = department_miashs
    )

@pytest.fixture
def group_type3 (db, department_reseaux : Department) -> GroupType :
    return GroupType.objects.create(
        name = "Groupe Type 3",
        department = department_reseaux
    )

@pytest.fixture
def group_type4 (db, department_langues : Department) -> GroupType :
    return GroupType.objects.create(
        name = "Groupe Type 4",
        department = department_langues
    )

@pytest.fixture
def course_type1 (db, group_type1 : GroupType, group_type2 : GroupType, group_type3 : GroupType, department_info : Department) -> CourseType :
    res = CourseType.objects.create(
        name = "Course Type 1",
        department = department_info
    )
    res.group_types.add(group_type3, group_type2, group_type1)
    res.save()
    return res

@pytest.fixture
def course_type2 (db, group_type4 : GroupType, department_langues : Department) -> CourseType :
    res = CourseType.objects.create(
        name = "Course Type 2",
        department = department_langues
    )
    res.group_types.add(group_type4)
    res.save()
    return res

@pytest.fixture
def course_type3 (db, group_type1 : GroupType, group_type2 : GroupType, group_type3 : GroupType, department_info : Department) -> CourseType :
    res = CourseType.objects.create(
        name = "Course Type 3",
        department = department_info
    )
    res.group_types.add(group_type3, group_type2, group_type1)
    res.save()
    return res

@pytest.fixture
def course_type4 (db, group_type4 : GroupType, department_langues : Department) -> CourseType :
    res = CourseType.objects.create(
        name = "Course Type 4",
        department = department_langues
    )
    res.group_types.add(group_type4)
    res.save()
    return res

""" Test Query
"""
def test_no_filter (client_query, course_type2 : CourseType, course_type4 : CourseType) :
    query = \
    """
        query{
            courseTypes (dept : \"LNG\") {
                edges {
                    node {
                        name
                    }
                }
            }
        }
    """
    res = execute_query(client_query, query, "courseTypes")
    data = get_data(res)
    assert course_type2.name in data["name"]
    assert course_type4.name in data["name"]

def test_with_filters (client_query, course_type1 : CourseType, course_type3 : CourseType) :
    query = \
    """
        query{
            courseTypes (dept : "INFO", name_Icontains : \"1\") {
                edges {
                    node {
                        name
                    }
                }
            }
        }
    """
    res = execute_query(client_query, query, "courseTypes")
    data = get_data(res)
    assert course_type1.name in data["name"]
    assert course_type3.name not in data["name"]

""" Test Mutations
"""
def test_mutations (db, client_query, department_langues : Department, department_info : Department, group_type1 : GroupType, group_type3 : GroupType, group_type4 : GroupType, capsys) :
    dpt_info_id = to_global_id("Department", department_info.id)
    dpt_langues_id = to_global_id("Department", department_langues.id)
    group_type1_id = to_global_id("GroupType", group_type1.id)
    group_type3_id = to_global_id("GroupType", group_type3.id)
    group_type4_id = to_global_id("GroupType", group_type4.id)
    create = \
    """
        mutation {
            createCourseType (
                name : "Course Type 5"
                department : \"""" + dpt_info_id \
                + """\" groupTypes : [\"""" + group_type1_id + "\", \"" + group_type3_id \
                + """\"] graded : true) {
                courseType {
                    id
                    name
                    department {
                        id
                        abbrev
                        name
                    }
                }
                groupTypes {
                    name
                }
            }
        }
    """

    global_id = execute_mutation(client_query, create, "createCourseType", "courseType")
    try:
        obj_id = from_global_id(global_id)[1]
        obj = CourseType.objects.get(id=obj_id)
        group_1_id = ""
        try :
            group_1 = obj.group_types.get(name = "Groupe Type 1")
            group_1_id = " , \"" + to_global_id("GroupType", group_1.id) + "\" "
        except GroupType.DoesNotExist :
            with capsys.disabled():
                print("Group Type 1 is not related to this object")
        
        with capsys.disabled():
            print("The object was created successfully")
        update = """
            mutation {
                updateCourseType (
                    id : \"""" + global_id + \
                    """\" name : "Course Type 7"
                    department : \"""" + dpt_langues_id + \
                    """\" groupTypes : [\"""" + group_type4_id + "\"" + group_1_id + \
                    """] graded : false
                ) {
                    courseType {
                    id
                    name
                    department {
                        id
                        abbrev
                        name
                    }
                    }
                    groupTypes {
                        name
                    }
                }
            } 
        """

        execute_mutation(client_query, update, "updateCourseType", "courseType")
        obj_updated = CourseType.objects.get(id=obj_id)
        assert obj.name != obj_updated.name
        assert obj.department.abbrev != obj_updated.department.abbrev
        assert obj.graded != obj_updated.graded
        assert len(obj_updated.group_types.all()) == 2 and obj_updated.group_types.all()[0].name == "Groupe Type 1" \
        and obj_updated.group_types.all()[1].name == "Groupe Type 4"
        with capsys.disabled():
            print("The object was updated successfully")

        delete = """
        mutation {
            deleteCourseType ( 
                id : \"""" + global_id + \
                """\" ) {
                courseType {
                    id
                }
            }
            }
        """
        execute_mutation(client_query, delete, "deleteCourseType", "courseType")
        try:
            obj_deleted = CourseType.objects.get(id=obj_id)
            with capsys.disabled():
                print("The object was not deleted")
        except CourseType.DoesNotExist:
            with capsys.disabled():
                print("The object was deleted successfully")


    except CourseType.DoesNotExist:
        with capsys.disabled():
            print("The object was not created")
        assert False

# courseType
""" name = models.CharField(max_length=50)
department = models.ForeignKey(
    Department, on_delete=models.CASCADE, null=True)
duration = models.PositiveSmallIntegerField(default=90)
pay_duration = models.PositiveSmallIntegerField(null=True, blank=True)
group_types = models.ManyToManyField(GroupType,
                                        blank=True,
                                        related_name="compatible_course_types")
graded = models.BooleanField(verbose_name=_('graded?'), default=False) """

# groupType
""" name = models.CharField(max_length=50)
department = models.ForeignKey(
Department, on_delete=models.CASCADE, null=True) """

# dept
""" name = models.CharField(max_length=50)
    abbrev = models.CharField(max_length=7) """