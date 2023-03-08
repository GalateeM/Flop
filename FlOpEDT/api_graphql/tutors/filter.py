from django_filters import FilterSet, CharFilter, NumberFilter
from people.models import Tutor
from base.models import Department, ScheduledCourse

class TutorFilter(FilterSet):
    # enlever required=True quand on fait un test de query
    dept = CharFilter(method = 'filter_dept')
    week = NumberFilter(method = 'filter_week')
    year = NumberFilter(method = 'filter_year')

    class Meta:
        model = Tutor
        fields = {
            'id' : ['exact'],
            'username' : ['icontains', 'istartswith'],
            'last_name' : ['icontains', 'istartswith'],
            'first_name' : ['icontains', 'istartswith'],
            'email' : ['icontains', 'istartswith']
        }
    
    def filter_dept(self, queryset, name, value):
        return queryset.filter(departments__in = Department.objects.filter(abbrev = value))

    def filter_week(self, queryset, name, value):
        return queryset.filter(pk__in = ScheduledCourse.objects.exclude(course__week = None).filter(course__week__nb = value).values("tutor"))

    def filter_year(self, queryset, name, value):
        return queryset.filter(pk__in = ScheduledCourse.objects.exclude(course__week = None).filter(course__week__year = value).values("tutor"))