import graphene

from quote.models import Quote, QuoteType

from api_graphql import lib
from .types import QuoteNode


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
        lib.assign_value_to_foreign_key(params,"quote_type", QuoteType, "create")

        quotes = Quote.objects.create(**params)
        return CreateQuote(quotes)