import json

from django_filters import FilterSet, CharFilter, NumberFilter

from people.models import Tutor

from base.models import Department, Course, ScheduledCourse


class TutorFilter(FilterSet):
    dept = CharFilter(method = 'filter_dept')
    week = CharFilter(method = 'filter_week')
    # week = NumberFilter(method = 'filter_week')
    # year = NumberFilter(method = 'filter_year')

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
        value = json.loads(value)
        if value["week"] > 53 or value["week"] < 0:
            return Tutor.objects.none()
        else:
            tutors_courses_id = Course.objects.exclude(week = None).filter(week__nb = value["week"], week__year = value["year"]).values_list("tutor__id", flat=True)
            tutors_scheduled_courses_id = ScheduledCourse.objects.exclude(course__week = None, course__tutor__id = None).filter(course__week__nb = value["week"], course__week__year = value["year"]).values_list("tutor__id", flat=True)
            tutors_id = tutors_courses_id.union(tutors_scheduled_courses_id)
            return queryset.filter(pk__in = tutors_id)

    # def filter_week(self, queryset, name, value):
    #     return queryset.filter(pk__in = ScheduledCourse.objects.exclude(course__week = None).filter(course__week__nb = value).values("tutor"))

    # def filter_year(self, queryset, name, value):
    #     return queryset.filter(pk__in = ScheduledCourse.objects.exclude(course__week = None).filter(course__week__year = value).values("tutor"))