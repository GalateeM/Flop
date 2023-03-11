from api_graphql.base import BaseMutation
from .create import CreateQuote
from .update import UpdateQuote
from .delete import DeleteQuote

class Mutation(BaseMutation):
    create_quote = CreateQuote.Field()
    update_quote = UpdateQuote.Field()
    delete_quote = DeleteQuote.Field()