from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from base.models import Module

class Module(DjangoObjectType):
    class Meta:
        

class DepartmentNode(DjangoObjectType):
    class Meta:
        model = Department
        filter_fields = {
            'id': ['exact'],
            'name': ['icontains', 'istartswith'],
            'abbrev': ['exact']
        }
        interfaces = (relay.Node, )

class TrainingProgrammeQL(DjangoObjectType):
    class Meta:
        model = TrainingProgramme
        fields = ('id', 'name', 'abbrev', 'department')
