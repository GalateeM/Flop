from pyexpat import model
from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from base.models import ModuleTutorRepartition

class TutorType(DjangoObjectType):
    class Meta:
        model = ModuleTutorRepartition
        fields = ("tutor",)
        filter_fields = {
            'tutor__departments__abbrev' : ['exact'],
            'tutor__username' : ['icontains', 'istartswith'],
            'tutor__last_name' : ['icontains', 'istartswith'],
            'tutor__first_name' : ['icontains', 'istartswith'],
            'tutor__email' : ['icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )
        