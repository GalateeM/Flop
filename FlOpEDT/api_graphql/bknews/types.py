from pyexpat import model
from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from displayweb.models import BreakingNews

class BknewsType(DjangoObjectType):

    class Meta:
        model = BreakingNews
        filter_fields = {
            'department__name' : ['icontains', 'istartswith'],
            'week' : ['exact'],
            'year' : ['exact'],
            'x_beg' : ['exact'],
            'x_end' : ['exact'],
            'y' : ['exact'],
            'txt' : ['icontains', 'istartswith'],
            'is_linked' : ['icontains', 'istartswith']
        }
        fields = ('x_beg', 'x_end', 'y', 'txt', 'is_linked')
        interfaces = (relay.Node, )
