from base.models import GroupType

def all_group_type(root, info):
    return GroupType.objects.all()
