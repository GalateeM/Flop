from api_graphql.base import BaseMutation
from .create import CreateBknews
from .update import UpdateBknews
from .delete import DeleteBknews

class Mutation(BaseMutation):
    create_bknews = CreateBknews.Field()
    update_bknews = UpdateBknews.Field()
    delete_bknews = DeleteBknews.Field()