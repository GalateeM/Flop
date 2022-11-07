from base.models import UserPreference

def all_user_preference(root, info):
    return UserPreference.objects.all()
