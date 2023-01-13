from graphene_django import DjangoObjectType
import graphene
from quote.models import Quote
from .types import QuoteNode

class createQuote(graphene.Mutation):
    class Arguments:
        quote = graphene.String()
        last_name = graphene.String()
        for_name = graphene.String()
        nick_name = graphene.String()
        desc_author = graphene.String()
        date = graphene.Date()
        header = graphene.String()
        quote_type__name = graphene.String()
        quote_type__abbrev = graphene.String()
        positive_votes = graphene.Int()
        negative_votes = graphene.Int()
        id_acc = graphene.String()
        status = graphene.String()

    quotes = graphene.Field(QuoteNode)

    @classmethod
    def mutate(cls, root, info, **user_data):
        quotes = Quote (
            quote = user_data.get('quote'),
            last_name = user_data.get('last_name'),
            for_name = user_data.get('for_name'),
            nick_name = user_data.get('nick_name'),
        )
        quotes.save()
        return createQuote(quotes=quotes)