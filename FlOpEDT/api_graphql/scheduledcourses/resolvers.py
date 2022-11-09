from base.models import ScheduledCourses

def all_courses(root, info):
    return ScheduledCourses.objects.all()
