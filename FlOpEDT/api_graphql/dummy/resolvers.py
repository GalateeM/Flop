from base.models import Department, TrainingProgramme
from .types import DummyDictNode

def all_departments(root, info):
    return Department.objects.all()

def all_training_programmes(root, info, **kwargs):
    print(kwargs)
    return TrainingProgramme.objects.all()

def resolve_dic(root, info):
    return DummyDictNode()
