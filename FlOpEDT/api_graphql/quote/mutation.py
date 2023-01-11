from api_graphql.base import BaseMutation
from .create import createQuote
from .update import UpdateQuote
from .delete import DeleteQuote

class Mutation(BaseMutation):
    """
    This class contains the fields of models that are supposed to be 
    mutated.
    """
    create_quote = createQuote.Field()
    update_quote = UpdateQuote.Field()
    delete_quote = DeleteQuote.Field()