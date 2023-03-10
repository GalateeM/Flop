from graphene_django import DjangoObjectType
import graphene
from django.db import models
from quote.models import Quote, QuoteType
from .types import QuoteNode
from api_graphql import lib
from graphql_relay import from_global_id

class UpdateQuote(graphene.mutation):
    class Arguments:
        id = graphene.ID(required=True)
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
    def mutate(cls, root, info,id, **params):
        id = from_global_id(id)[1]
        quote_set = Quote.objects.filter(id=id)
        if quote_set:

            #foreignKEY

            lib.assign_value_to_foreign_key(params, "quote_type", QuoteType, "update")

            quote_set.update(**params)
            quotes = quote_set.first()
            quotes.save()

            return UpdateQuote(quotes)
        else:
            print("quote with the given Id does not exist in the database")

