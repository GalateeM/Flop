from django_filters import FilterSet, NumberFilter, CharFilter

from base.models import ScheduledCourse


class ScheduledCourseFilter(FilterSet):
    week = NumberFilter(required = True, method = 'filter_week')
    year = NumberFilter(required = True, method = 'filter_year') 
    dept = CharFilter(method = 'filter_dept')
    class Meta:
        model = ScheduledCourse
        fields = {
            'id' : ['exact'],
            'room__name': ['icontains', 'istartswith'],
            'day': ['exact'],
            'course__module__abbrev': ['icontains', 'istartswith'],
            'tutor__username': ['icontains', 'istartswith'],
            'start_time' : ['exact'],
            'no' : ['exact'],
            'noprec': ['exact'],
            'work_copy': ['exact']
        }
    
    def filter_week(self, queryset, name, value):
        return queryset.exclude(course__week = None).filter(course__week__nb = value)

    def filter_year(self, queryset, name, value):
        return queryset.exclude(course__week = None).filter(course__week__year = value)

    def filter_dept(self, queryset, name, value):
        return queryset.exclude(course__type__department = None).exclude(course__module__train_prog__department = None). \
        filter(course__module__train_prog__department__abbrev = value)