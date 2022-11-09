from base.models import CourseType

def all_course_type(root, info):
    return CourseType.objects.all()
