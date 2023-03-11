from api_graphql.base import BaseMutation
from .create import CreateTrainingProgramme
from .update import UpdateTrainingProgramme
from .delete import DeleteTrainingProgramme

class Mutation(BaseMutation):
    create_training_programme = CreateTrainingProgramme.Field()
    update_training_programme = UpdateTrainingProgramme.Field()
    delete_training_programme = DeleteTrainingProgramme.Field()