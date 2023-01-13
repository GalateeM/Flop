from graphene.types.objecttype import ObjectType, ObjectTypeOptions
from graphql_relay import from_global_id

class BaseQuery(ObjectType):
    pass


class BaseMutation(ObjectType):
    def get_form_kwargs(cls, root, info, **input):
        kwargs = {"data": input}

        global_id = input.pop("id", None)
        if global_id:
            node_type, pk = from_global_id(global_id)
            instance = cls._meta.model._default_manager.get(pk=pk)
            kwargs["instance"] = instance

        return kwargs


class BaseSubscription(ObjectType):
    pass
