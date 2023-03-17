from django_filters import FilterSet, CharFilter, NumberFilter, BooleanFilter

from base.models import Course, ScheduledCourse


class UnscheduledCourseFilter(FilterSet):
    year = NumberFilter(method='filter_year')
    week = NumberFilter(method='filter_week')
    dept = CharFilter(method='filter_department')

    class Meta:
        model = Course
        fields = {
            'id' : ['exact'],
            'type__name' : ['icontains', 'istartswith'],
            'room_type__name' : ['icontains', 'istartswith'],
            'no' : ['exact'],
            'tutor__username' : ['exact'],
            'tutor__first_name' : ['icontains', 'istartswith'],
            'module__name' : ['icontains', 'istartswith'],
            'module__abbrev' : ['exact'],
            'modulesupp__name' : ['icontains', 'istartswith'],
            'modulesupp__abbrev' : ['exact'],
            'pay_module__name' : ['icontains', 'istartswith'],
            'pay_module__abbrev' : ['exact'],
        }
        exclude = ('suspens', 'show_id')
    
    def filter_week(self, queryset, name, value):
        print("week")
        return queryset.exclude(week = None).filter(week__nb=value)
    
    def filter_year(self, queryset, name, value):
        print("year")
        return queryset.exclude(week = None).filter(week__year=value)
    
    def filter_department(self, queryset, name, value):
        print("dept")
        return queryset.filter(module__train_prog__department__abbrev=value)

    def filter_queryset(self, queryset):
        courses_ids = queryset.values_list('id')
        scheduled_courses = ScheduledCourse.objects.filter(course__id__in = courses_ids)
        scheduled_course_ids = scheduled_courses.values_list('course__id', flat=True)
        return queryset.exclude(pk__in=scheduled_course_ids)