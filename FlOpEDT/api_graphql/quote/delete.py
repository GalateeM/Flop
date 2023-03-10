from graphene_django import DjangoObjectType
import graphene
from django.db import models
from quote.models import Quote, QuoteType
from .types import QuoteNode
from api_graphql import lib
from graphql_relay import from_global_id

class DeleteQuote(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    quotes = graphene.Field(QuoteType)


    @classmethod
    def mutate(cls,root, info, id):
        id = from_global_id(id) [1]
        try:
            quotes = Quote.objects.get(id=id)
            quotes.delete()

            return DeleteQuote(quotes)
        except Quote.DoesNotExist:
            print("Quote with the given Id does not exist")
