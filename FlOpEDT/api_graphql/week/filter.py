from django_filters import FilterSet

from base.models import Week


class WeekFilter(FilterSet):
    class Meta:
        model = Week
        fields = {
            'id' : ['exact'],
            'nb' : ['exact'],
            'year' : ['exact']
        }