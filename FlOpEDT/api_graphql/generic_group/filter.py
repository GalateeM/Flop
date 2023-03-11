from django_filters import FilterSet, CharFilter

from base.models import GenericGroup


class GenericGroupFilter(FilterSet):
    dept = CharFilter(required = True, method = 'filter_dept')

    class Meta:
        model = GenericGroup
        fields = {
            'id' : ["exact"],
            'name' : ['icontains', 'istartswith'],
            'train_prog__name' : ['icontains', 'istartswith'],
            'type__name' : ['icontains', 'istartswith'],
            'size' : ['exact']
        }
    
    def filter_dept(self, queryset, name, value):
        return queryset.exclude(type__department = None).exclude(train_prog__department = None) .filter(train_prog__department__abbrev = value)