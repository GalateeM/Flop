from django_filters import FilterSet
from base.models import RoomType

class RoomTypeFilter(FilterSet):
    class Meta:
        model = RoomType
        fields = {
            'id' : ['exact'],
            'department__name' : ['icontains', 'istartswith'],
            'department__abbrev' : ['exact'],
            'name' : ['istartswith', 'icontains']
        }
