from graphene_django import DjangoObjectType
import graphene
from django.db import models
from quote.models import  QuoteType
from .types import QuoteTypeNode
from api_graphql import lib
from graphql_relay import from_global_id

class CreateQuoteType(graphene.mutation):
    class Arguments:
        name = graphene.String(graphene.ID, required = True)
        abbrev = graphene.String(graphene.ID)
        parent = graphene.Argument(graphene.ID)

    quote_types = graphene.Field(QuoteTypeNode)

    @classmethod
    def mutate(cls, root, info, **params):

        #foreignkey

        lib.assign_value_to_foreign_key(params, "parent", QuoteType, "create")

        quote_types = QuoteType.objects.create(**params)
        return CreateQuoteType(quote_types)
       


