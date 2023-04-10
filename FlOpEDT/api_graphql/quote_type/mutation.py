from api_graphql.base import BaseMutation
from .create import CreateQuoteType
from .update import UpdateQuoteType
from .delete import DeleteQuoteType

class Mutation(BaseMutation):
    create_quote_type = CreateQuoteType.Field()
    update_quote_type = UpdateQuoteType.Field()
    delete_quote_type = DeleteQuoteType.Field()