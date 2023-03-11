from graphene_django import DjangoObjectType
import graphene
from django.db import models
from quote.models import Quote, QuoteType
from .types import QuoteNode
from api_graphql import lib

class CreateQuote(graphene.Mutation):
    class Arguments:
        quote = graphene.String(required= True)
        last_name = graphene.String()
        for_name = graphene.String()
        nick_name = graphene.String()
        desc_author = graphene.String()
        date = graphene.String()
        header = graphene.String()
        quote_type = graphene.Argument(graphene.ID)
        positive_votes = graphene.Int()
        negative_votes = graphene.Int()
        id_acc = graphene.Int()

    quotes = graphene.Field(QuoteNode)

    @classmethod
    def mutate(cls, root, info, **params):

        #foreignkey
        lib.assign_value_to_foreign_key(params,"quote_type", QuoteType, "create")

        quotes = Quote.objects.create(**params)
        return CreateQuote(quotes)