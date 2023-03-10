from graphene_django import DjangoObjectType
import graphene
from django.db import models
from quote.models import  QuoteType
from .types import QuoteTypeNode
from api_graphql import lib
from graphql_relay import from_global_id

class UpdateQuoteType(graphene.mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(graphene.ID)
        abbrev = graphene.String(graphene.ID)
        parent = graphene.Argument(graphene.ID)

    quote_types = graphene.Field(QuoteTypeNode)

    @classmethod
    def mutate(cls, root, info,id, **params):
        id = from_global_id(id)[1]
        quote_type_set = QuoteType.objects.filter(id=id)

        if quote_type_set:

            #foreignkey
            lib.assign_value_to_foreign_key(params, "parent", QuoteType, "update")

            quote_type_set.update(**params)
            quote_types = quote_type_set.first()
            quote_types.save()

            return UpdateQuoteType(quote_types)
        else:
            print("Quote Type with the given Id doesn't exist")
