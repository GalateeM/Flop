import graphene

from quote.models import QuoteType

from api_graphql import lib
from .types import QuoteTypeNode


class CreateQuoteType(graphene.Mutation):
    class Arguments:
        name = graphene.String(required = True)
        abbrev = graphene.String()
        parent = graphene.Argument(graphene.ID)

    quote_types = graphene.Field(QuoteTypeNode)

    @classmethod
    def mutate(cls, root, info, **params):
        lib.assign_value_to_foreign_key(params, "parent", QuoteType, "create")

        quote_types = QuoteType.objects.create(**params)
        return CreateQuoteType(quote_types)