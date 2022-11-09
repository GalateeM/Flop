from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from base.models import Course

class CourseNode(DjangoObjectType):

    class Meta:
        model = Course
        filter_fields = {
            'type__name' : ['icontains', 'istartswith'],
            'room_type__name' : ['icontains', 'istartswith'],
            'no' : ['exact'],
            'tutor__username' : ['exact'],
            'tutor__first_name' : ['icontains', 'istartswith'],
            'supp_tutor__username' : ['exact'],
            'supp_tutor__first_name' : ['icontains', 'istartswith'],
            'groups__name' : ['icontains', 'istartswith'],
            'module__name' : ['icontains', 'istartswith'],
            'module__abbrev' : ['exact'],
            'modulesupp__name' : ['icontains', 'istartswith'],
            'modulesupp__abbrev' : ['exact'],
            'pay_module__name' : ['icontains', 'istartswith'],
            'pay_module__abbrev' : ['exact'],
            'week__nb' : ['exact'],
            'week__year' : ['exact']
        }
        exclude = ('suspens', 'show_id')
        interfaces = (relay.Node, )
