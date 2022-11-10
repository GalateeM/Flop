from base.models import Room, Department

def all_rooms(root, info, dept):
    print(dept)
    return Room.objects.filter(departments__in = Department.objects.filter(abbrev = dept))
