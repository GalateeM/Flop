from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from base.models import Module


class ModuleNode(DjangoObjectType):
    class Meta:
        model = Module
        filter_fields = {
            'id': ['exact'],
            'name': ['icontains', 'istartswith'],
            'abbrev': ['exact'],
            'head': ['exact'],
            'train_prog': ['exact'],
            'period': ['exact'],
            'url': ['exact'],
            'description': ['exact']
        }
        interfaces = (relay.Node, )
