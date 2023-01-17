from graphene import Schema

from .auto import schema_operations_builder

ALL_QUERIES = schema_operations_builder(
    operationName='Query',
    operationModule='query',
    operationBase='BaseQuery',
    clsName='Query'
)
ALL_MUTATIONS = schema_operations_builder(
    operationName='Mutation',
    operationModule='mutation',
    operationBase='BaseMutation',
    clsName='Mutation'
)

schema = Schema(query=ALL_QUERIES, mutation=ALL_MUTATIONS)
