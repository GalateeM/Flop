from django_filters import FilterSet

from displayweb.models import BreakingNews


class BknewsFilter(FilterSet):
    class Meta:
        model = BreakingNews
        fields = {
            'id' : ["exact"],
            'department__name' : ['icontains', 'istartswith'],
            'department__abbrev' : ['exact'],
            'week' : ['exact'],
            'year' : ['exact'],
            'x_beg' : ['exact'],
            'x_end' : ['exact'],
            'y' : ['exact'],
            'txt' : ['icontains', 'istartswith'],
            'is_linked' : ['icontains', 'istartswith'],
            'fill_color' : ['exact'],
            'strk_color' : ['exact']
        }