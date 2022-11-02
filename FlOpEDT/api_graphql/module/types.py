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
            'head': ['exact'],
            'ppn' : ['icontains'],
            'train_prog__abbrev': ['exact'],
            'train_prog__name': ['icontains'],
            'period__name': ['exact'],
            'url' : ['exact', 'icontains'],
            'description': ['icontains', 'exact']
        }
        interfaces = (relay.Node, )
