from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import UserPreferenceNode


class Query(BaseQuery):
    """
        Une seule requête pour UserDefaultPreference, UserActualPreference et UserSingularPreference\n
        On a Default si on ne filtre que par le username\n
        On a Actual ou Singular si on rajoute week ou year en plus\n
        Pour l'instant, on ne peut pas filtrer par département (à implémenter)
    """
    user_preferences = DjangoFilterConnectionField(
        UserPreferenceNode,
        description="A list of user preference.",
        resolver=resolve.all_user_preference
    )
