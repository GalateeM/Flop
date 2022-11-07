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
            'id' : ['exact'],
            'x__beg' : ['exact'],
            'x__end' : ['exact'],
            'y' : ['exact'],
            'txt' : ['icontains', 'istartswith'],
            'is__linked' : ['icontains', 'istartswith'],
        }
        fields = ('id', 'x__deg', 'x__end', 'y', 'txt', 'is__linked')
        interfaces = (relay.Node, )