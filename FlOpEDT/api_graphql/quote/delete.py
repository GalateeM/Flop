import graphene
from graphql_relay import from_global_id

from quote.models import Quote

from .types import QuoteNode


class DeleteQuote(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    quotes = graphene.Field(QuoteNode)

    @classmethod
    def mutate(cls,root, info, id):
        id = from_global_id(id) [1]
        try:
            quotes = Quote.objects.get(id=id)
            quotes.delete()

            return DeleteQuote(quotes)
        except Quote.DoesNotExist:
            print("Quote with the given Id does not exist")
