import json

from django_filters import FilterSet, CharFilter, NumberFilter

from base.models import Module, Course


class ModuleFilter(FilterSet):
    dept = CharFilter(method = 'filter_dept', required = True)
    week = CharFilter(method = 'filter_week')
    
    class Meta:
        model = Module
        fields = {
            'id' : ["exact"],
            'name': ['icontains', 'istartswith'],
            'abbrev': ['exact'],
            'ppn' : ['icontains'],
            'head__username' : ['exact'],
            'head__first_name' : ['icontains'],
            'train_prog__abbrev': ['exact'],
            'period__name': ['exact'],
            'url' : ['exact', 'icontains']
        }
        exclude = ('description',)

    def filter_dept(self, queryset, name, value):
        return queryset.exclude(period__department = None, train_prog__department = None).filter(period__department__abbrev = value, train_prog__department__abbrev = value)

    def filter_week(self, queryset, name, value):
        value = json.loads(value)
        if value["week"] > 53 or value["week"] < 0:
            return Module.objects.none()
        else:
            modules_id = Course.objects.filter(week__nb = value["week"], week__year = value["year"]).values_list("module__id")
            return queryset.filter(pk__in = modules_id)