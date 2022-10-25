from base.models import Department, TrainingProgramme

def all_departments(root, info):
    return Department.objects.all()

def all_training_programmes(root, info):
    return TrainingProgramme.objects.all()
