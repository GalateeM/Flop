from django_filters import FilterSet

from base.models import Period


class PeriodFilter(FilterSet):
    class Meta:
        model = Period
        fields = {
            'id' : ["exact"],
            'department__name' : ['icontains', 'istartswith'],
            'department__abbrev' : ['exact'],
            'name' : ['exact', "icontains"]
        }