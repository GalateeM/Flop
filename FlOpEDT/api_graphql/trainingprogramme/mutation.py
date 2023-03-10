from api_graphql.base import BaseMutation
from .create import CreateTrainingProgramme
from .update import UpdateTrainingProgramme
from .delete import DeleteTrainingProgramme

class Mutation(BaseMutation):
    """
    This class contains the fields of models that are supposed to be 
    mutated.
    """

    create_training_programme = CreateTrainingProgramme.Field()
    update_training_programme = UpdateTrainingProgramme.Field()
    delete_training_programme = DeleteTrainingProgramme.Field()