import graphene
from graphql_relay import from_global_id

from base.models import TrainingProgramme, Department

from api_graphql import lib
from .types import TrainingProgrammeType


class UpdateTrainingProgramme(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
        name = graphene.String()
        abbrev = graphene.String()
        department = graphene.Argument(graphene.ID)

    training_programme = graphene.Field(TrainingProgrammeType)

    @classmethod
    def mutate(cls, root, info, id, **params):
        id = from_global_id(id)[1]
        training_programme_set = TrainingProgramme.objects.filter(id=id)
        if training_programme_set:
            lib.assign_value_to_foreign_key(params, "department", Department, "create")
            
            training_programme_set.update(**params)
            training_programme = training_programme_set.first()
            training_programme.save()

            return UpdateTrainingProgramme(training_programme)
        else:
            print('Training programme with given ID does not exist in the database')
