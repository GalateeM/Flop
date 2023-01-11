from graphene_django import DjangoObjectType
import graphene
from quote.models import Quote
from .types import QuoteNode

class UpdateQuote(graphene.Mutation):
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
        positive_votes = graphene.Integer()
        negative_votes = graphene.Integer()
        id_acc = graphene.String()
        status = graphene.String()

    quotes = graphene.Field(QuoteNode)

    @classmethod
    def mutate(cls, root, info, nick_name, **update_data):
        quotes = Quote.objects.filter(nick_name=nick_name)
        if quotes:
            params = update_data
            quotes.update(**{k: v for k, v in params.items() if params[k]})
            return UpdateQuote(quotes=quotes.first())

        else:
            print('Quote with given nickname does not exist in the database')