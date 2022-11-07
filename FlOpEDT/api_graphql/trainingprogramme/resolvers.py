from base.models import TrainingProgramme

def all_trainingprogramme(root, info):
    return TrainingProgramme.objects.all()