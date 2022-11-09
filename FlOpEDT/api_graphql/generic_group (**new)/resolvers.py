from base.models import GenericGroup

def all_generic_group(root, info):
    return GenericGroup.objects.all()
