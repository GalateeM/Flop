from base.models import RoomType

def all_room_type(root, info):
    return RoomType.objects.all()
