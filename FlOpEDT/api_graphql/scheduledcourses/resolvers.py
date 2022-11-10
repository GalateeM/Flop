from base.models import ScheduledCourse

def all_scheduled_courses(root, info):
    return ScheduledCourse.objects.all()
