from graphene_django import DjangoObjectType
import graphene
from quote.models import Quote
from .types import QuoteNode

class DeleteQuote(graphene.Mutation):
        class Arguments:
            # id = graphene.ID()
            nick_name = graphene.String()

        quotes= graphene.Field(QuoteNode)

        @classmethod
        def mutate(cls, root, info, nick_name):
            quotes = Quote.objects.get(nick_name=nick_name)
            quotes.delete()
            return DeleteQuote(quotes)