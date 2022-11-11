from graphene import relay
from graphene_django import DjangoObjectType
from displayweb.models import BreakingNews
from .filter import BknewsFilter

class BknewsType(DjangoObjectType):
    class Meta:
        model = BreakingNews
        filterset_class = BknewsFilter
        interfaces = (relay.Node, )
