from base.models import Period

def all_periods(root, info):
    return Period.objects.all()
