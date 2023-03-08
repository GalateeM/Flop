from django_filters import FilterSet
from quote.models import QuoteType

class QuoteTypeFilter(FilterSet):
    class Meta:
        model = QuoteType
        fields = {
            'id' : ['exact'],
            'name' : ['exact', 'icontains', 'istartswith'],
            'abbrev' : ['exact'],
            'parent__abbrev' : ['exact'],
            'parent__name' : ['exact', 'icontains', 'istartswith']
        }