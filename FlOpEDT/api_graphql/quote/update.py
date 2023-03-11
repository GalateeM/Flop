from graphene_django import DjangoObjectType
import graphene
from django.db import models
from quote.models import Quote, QuoteType
from .types import QuoteNode
from api_graphql import lib
from graphql_relay import from_global_id

class UpdateQuote(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        quote = graphene.String()
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

