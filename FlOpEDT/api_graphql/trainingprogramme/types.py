from graphene import ObjectType, Int, String, List, lazy_import, relay
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from base.models import TrainingProgramme

class TrainingProgramme(DjangoObjectType):
    class Meta:
        model = TrainingProgramme
        filter_fields = {
            'abbrev': ['exact'],
    
        }
        fields = ('abbrev',)
        interfaces = (relay.Node, )
