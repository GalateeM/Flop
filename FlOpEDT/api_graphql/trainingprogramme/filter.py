from django_filters import FilterSet, CharFilter
from base.models import TrainingProgramme

class TrainingProgrammeFilter(FilterSet):
    dept = CharFilter(required = True, method = 'filter_dept')

    class Meta:
        model = TrainingProgramme
        fields = {
            'id' : ['exact'],
            'abbrev': ['exact']
        }

    def filter_dept(self, queryset, name, value):
        return queryset.exclude(department = None).filter(department__abbrev = value)