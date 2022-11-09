from base.models import Room

def all_rooms(root, info):
    return Room.objects.all()
