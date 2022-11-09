from base.models import Week

def all_weeks(root, info):
    return Week.objects.all()
