from people.models import Tutor
#from base.models import Department, Week

def all_tutors(root, info): # , dept, week, years  (dept n'est pas dans la class Department)
    return Tutor.object.all()

def all_username(root, info):
    return Tuto.object.all()