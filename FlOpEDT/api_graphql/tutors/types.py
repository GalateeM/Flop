from pyexpat import model
from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from people.models import Tutor

class TutorType(DjangoObjectType):

    class Meta:
        model = Tutor
        filter_fields = {
            'username' : ['icontains', 'istartswith'],
            'last__name' : ['icontains', 'istartswith'],
            'first__name' : ['icontains', 'istartswith'],
            'email' : ['icontains', 'istartswith'],
        }
        fields = ('username', 'last__name', 'first__name', 'email')
        interfaces = (relay.Node, )
        