from pyexpat import model
from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from base.models import Department

class DepartmentType(DjangoObjectType):

    class Meta:
        model = Department
        filter_fields = {
            'name' : ['icontains', 'istartswith'],
            'abbrev' : ['exact']
        fields = '__all__'
        interfaces = (relay.Node, )
        
