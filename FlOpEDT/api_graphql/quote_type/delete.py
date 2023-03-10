from graphene_django import DjangoObjectType
import graphene
from django.db import models
from quote.models import  QuoteType
from .types import QuoteTypeNode
from api_graphql import lib
from graphql_relay import from_global_id

class DeleteQuoteType(graphene.mutation):
    class Arguments:
        id = graphene.ID(required=True)

    quote_types = graphene.Field(QuoteTypeNode)

    @classmethod
    def mutate(cls,root, info, id):
        id = from_global_id(id) [1]

        try:
            quote_types = QuoteType.objects.get(id=id)
            quote_types.delete()

            return DeleteQuoteType(quote_types)
        except QuoteType.DoesNotExist:
            print("QuoteType with the given Id does not exist")