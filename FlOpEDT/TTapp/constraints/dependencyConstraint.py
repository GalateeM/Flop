from TTapp.constraint import Constraint
from TTapp.constraint_type import ConstraintType


class DependencyConstraint(Constraint):
    def __init__(self, course1, course2, slot1, slot2):
        self.course1 = course1
        self.course2 = course2
        self.slot1 = slot1
        self.slot2 = slot2
        Constraint.__init__(self, constraint_type=ConstraintType.DEPENDANCE,
                            courses=[course1, course2], slots=[slot1, slot2])

    def get_info_summary(self):
        output = "Problème de dépendance entre les cours suivants:\n\t%s\n\t%s"
        dimensions_to_fill = ["courses_1", "courses_2"]
        return output, dimensions_to_fill

    def get_summary_format(self):
        output = "\tProblème de dépendance entre les cours suivants:\n%s"
        dimensions = ["courses"]
        return output, dimensions
