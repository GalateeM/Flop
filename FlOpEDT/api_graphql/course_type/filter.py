from django_filters import FilterSet, CharFilter

from base.models import CourseType, Department


class CourseTypeFilter(FilterSet):
    dept = CharFilter(required = True, method = 'filter_dept')

    class Meta:
        model = CourseType
        fields = {
            'id' : ['exact'],
            'name' : ['icontains', 'istartswith'],
            'duration' : ['exact'],
            'pay_duration' : ['exact'],
            'graded' : ['exact'],
            'group_types__name' : ['icontains', 'istartswith']
        }

    def filter_dept(self, queryset, name, value):
        return queryset.filter(department__in = Department.objects.filter(abbrev = value))