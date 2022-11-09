from graphene import ObjectType, Int, String, List, lazy_import, relay, \
    InputObjectType
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from . import resolvers as resolve

from base.models import Department, TrainingProgramme


class DepartmentNode(DjangoObjectType):
    class Meta:
        model = Department
        filter_fields = {
            'id': ['exact'],
            'name': ['icontains', 'istartswith'],
            'abbrev': ['exact']
        }
        interfaces = (relay.Node, )


class TrainingProgrammeQL(DjangoObjectType):
    class Meta:
        model = TrainingProgramme
        fields = ('id', 'name', 'abbrev', 'department')


class DummyDictNode(ObjectType):
    out = GenericScalar()

    def resolve_out(root, info):
        ret = dict()
        ret["pouet"] = {"w": 10}
        ret["poot"] = 11
        return ret
