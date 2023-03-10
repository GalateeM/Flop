from graphene_django import DjangoObjectType
import graphene
from django.db import models
from quote.models import Quote, QuoteType
from .types import QuoteNode
from api_graphql import lib

class CreateQuote(graphene.mutation):
    class Arguments:
        quote = graphene.String(graphene.ID, required= True)
        last_name = graphene.String(graphene.ID)
        for_name = graphene.String(graphene.ID)
        nick_name = graphene.String(graphene.ID)
        desc_author = graphene.String(graphene.ID)
        date = graphene.String(graphene.ID)
        header = graphene.String(graphene.ID)
        quote_type = graphene.Argument(graphene.ID)
        positive_votes = graphene.Int(graphene.ID)
        negative_votes = graphene.Int(graphene.ID)
        id_acc = graphene.Int(graphene.ID)

    quotes = graphene.Field(QuoteNode)

    @classmethod
    def mutate(cls, root, info, **params):

        #foreignkey
        lib.assign_value_to_foreign_key(params,"quote_type", QuoteType, "create")

        quotes = Quote.objects.create(**params)
        return CreateQuote(quotes)