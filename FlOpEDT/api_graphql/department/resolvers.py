from base.models import Department
#from base.models import Department, Week

def all_departments(root, info): # , dept, week, years  (dept n'est pas dans la class Department)
    return Department.objects.all()
