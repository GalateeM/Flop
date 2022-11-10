from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from base.models import ScheduledCourse

class ScheduledCourseNode(DjangoObjectType):
    class Meta:
        model = ScheduledCourse
        filter_fields = {
            'room__name': ['icontains', 'istartswith'],
            'day': ['exact'],
            'course__module__abbrev': ['icontains', 'istartswith'],
            'tutor__username': ['icontains', 'istartswith'],
            'start_time' : ['exact'],
            'no' : ['exact'],
            'noprec': ['exact'],
            'work_copy': ['exact']
        }
    
        interfaces = (relay.Node, )
