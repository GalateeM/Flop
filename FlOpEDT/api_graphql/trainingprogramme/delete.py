import graphene
from graphql_relay import from_global_id

from base.models import TrainingProgramme

from .types import TrainingProgrammeType


class DeleteTrainingProgramme(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
    
    training_programme = graphene.Field(TrainingProgrammeType)


    @classmethod
    def mutate(cls,root, info, id):
        id = from_global_id(id) [1]
        try:
            training_programme = TrainingProgramme.objects.get(id=id)
            training_programme.delete()
            return DeleteTrainingProgramme(training_programme)
        
        except TrainingProgramme.DoesNotExist:
            print('Training programme with given ID does not exist in the database')