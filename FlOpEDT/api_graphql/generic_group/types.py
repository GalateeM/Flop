from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from base.models import GenericGroup

class GenericGroupNode(DjangoObjectType):

    class Meta:
        model = GenericGroup
        filter_fields = {
            'name' : ['icontains', 'istartswith'],
            'train_prog__name' : ['icontains', 'istartswith'],
            'type__name' : ['icontains', 'istartswith'],
            'size' : ['exact']
        }
        fields = '__all__'
        interfaces = (relay.Node, )
