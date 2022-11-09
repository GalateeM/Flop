from base.models import Course

def all_courses(root, info):
    return Course.objects.all()
