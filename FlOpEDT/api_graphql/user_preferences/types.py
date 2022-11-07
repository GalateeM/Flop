from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from base.models import UserPreference

class UserPreferenceNode(DjangoObjectType):
    class Meta:
        model = UserPreference
        filter_fields = {
            'user__username' : ['exact', 'icontains'],
            'user__first_name' : ['icontains', 'istartswith'], 
            'week__nb' : ['exact'], 
            'week__year' : ['exact']
        }
        fields = "__all__"
        interfaces = (relay.Node, )