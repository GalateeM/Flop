from django_filters import FilterSet, CharFilter, NumberFilter
from base.models import UserPreference, Department

class UserPreferenceFilter(FilterSet):
    dept = CharFilter(method = 'filter_dept')
    week = NumberFilter(required = True, method = 'filter_week')
    year = NumberFilter(required = True, method = 'filter_year')

    class Meta:
        model = UserPreference
        fields = {
            'user__username' : ['exact', 'icontains'],
            'user__first_name' : ['icontains', 'istartswith'], 
            'week__nb' : ['exact'], 
            'week__year' : ['exact']
        }

    def filter_dept(self, queryset, name, value):
        return queryset.filter(user__departments__in = Department.objects.filter(abbrev = value))

    def filter_week(self, queryset, name, value):
        return queryset.exclude(week = None).filter(week__nb = value)

    def filter_year(self, queryset, name, value):
        return queryset.exclude(week = None).filter(week__year = value)