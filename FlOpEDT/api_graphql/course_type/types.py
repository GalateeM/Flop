from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from base.models import CourseType

class CourseTypeNode(DjangoObjectType):

    class Meta:
        model = CourseType
        filter_fields = {
            'name' : ['icontains', 'istartswith'],
            'department__name' : ['icontains', 'istartswith'],
            'department__abbrev' : ['exact'],
            'duration' : ['exact'],
            'pay_duration' : ['exact'],
            'graded' : ['exact'],
            'group_types__name' : ['icontains', 'istartswith']
        }
        fields = ('name', 'department')
        interfaces = (relay.Node, )
