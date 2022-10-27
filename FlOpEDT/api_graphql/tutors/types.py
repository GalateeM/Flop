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
            'last_name' : ['icontains', 'istartswith'],
            'first_name' : ['icontains', 'istartswith'],
            'email' : ['icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )
        #fields = ('username',)

class TutorUsername(DjangoObjectType):
    class Meta:
        model = Tutor
        filter_fields = {
            'username' : ['icontains', 'istartswith'],
        }