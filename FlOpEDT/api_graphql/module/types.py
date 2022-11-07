from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from base.models import Module

class ModuleNode(DjangoObjectType):
    class Meta:
        model = Module
        filter_fields = {
            'name': ['icontains', 'istartswith'],
            'abbrev': ['exact'],
            'ppn' : ['icontains'],
            'head__username' : ['exact'],
            'head__first_name' : ['icontains'],
            'train_prog__abbrev': ['exact'],
            'period__name': ['exact'],
            'url' : ['exact', 'icontains'],
        }
        exclude = ('description',)
        interfaces = (relay.Node, )
