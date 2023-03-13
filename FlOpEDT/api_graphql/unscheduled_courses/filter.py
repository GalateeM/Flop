from django_filters import FilterSet, CharFilter, NumberFilter

from base.models import Course, ScheduledCourse


class UnscheduledCourseFilter(FilterSet):
    year = NumberFilter(field_name='week__year')
    week = NumberFilter(field_name='week__nb')
    work_copy = NumberFilter(field_name='work_copy')
    dept = CharFilter(field_name='module__train_prog__department__abbrev')

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
        
    def filter_queryset(self, queryset):
        scheduled_courses = ScheduledCourse.objects.all()
        # Filtering by year
        year = self.request.GET.get('year', None)
        if year:
            queryset = queryset.exclude(week = None).filter(week__year=year)
            scheduled_courses = scheduled_courses.exclude(course__week = None).filter(course__week__year=year)

        # Filtering by week
        week = self.request.GET.get('week', None)
        if week:
            queryset = queryset.exclude(week = None).filter(week__nb=week)
            scheduled_courses = scheduled_courses.exclude(course__week = None).filter(course__week__nb=week)

        # Filtering by work_copy
        work_copy = self.request.GET.get('work_copy', None)
        if work_copy:
            queryset = queryset.filter(work_copy=work_copy)
            scheduled_courses = scheduled_courses.filter(course__work_copy=work_copy)

        # Filtering by department
        dept = self.request.GET.get('dept', None)
        if dept:
            queryset = queryset.exclude(type__department = None).filter(module__train_prog__department__abbrev=dept)
            scheduled_courses = scheduled_courses.exclude(course__type__department = None).filter(course__module__train_prog__department__abbrev=dept)

        # Exclude scheduled courses
        scheduled_course_ids = scheduled_courses.values_list('course__id', flat=True)
        print(f"len cou = {len(queryset)}")
        print(f"len unsc_cou_excp = {len(queryset) - len(scheduled_course_ids)}")
        queryset = queryset.exclude(pk__in=scheduled_course_ids)
        print(f"len sch_cou = {len(scheduled_course_ids)}")
        print(f"len unsc_cou = {len(queryset)}")
        return queryset