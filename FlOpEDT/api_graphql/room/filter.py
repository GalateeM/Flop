from django_filters import FilterSet, CharFilter
from base.models import Room, Department

class RoomFilter(FilterSet):
    dept = CharFilter(method = 'filter_room')
    week  =C

    class Meta:
        model = Room
        fields = '__all__'

    def filter_room(self, queryset, name, value):
        return queryset.filter(departments__in = Department.objects.filter(abbrev = value))