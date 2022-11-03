from base.models import ModuleTutorRepartition

def all_tutors(root, info):
    return ModuleTutorRepartition.objects.all()