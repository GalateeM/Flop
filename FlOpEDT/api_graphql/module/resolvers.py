from base.models import Module

def all_modules(root, info):
    return Module.objects.all()
