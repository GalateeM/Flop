import os
import importlib
from inspect import getmembers, isclass
from graphene import ObjectType
import logging

logger = logging.getLogger(__name__)


def schema_operations_builder(operationName, operationModule, operationBase, clsName):
    """
    Cette fonction fabrique un type unique, qui porte le nom operationName, qui contient toutes les classes
    qui s'appellent avec un nom contenant clsName (sauf la classe operationBase) et ayant comme propriétés toutes les
    propriétés de ces classes
    """
    op_base_classes = build_base_classes(operationName, operationModule, operationBase, clsName)

    if len(op_base_classes) <= 1:
        raise ValueError("Found no '{0}' classes in '{1}' module of subdirectories.".format(
            operationBase, operationModule
        ))

    properties = {}
    # filter on scopes before this
    for base_class in op_base_classes:
        properties.update(base_class.__dict__['_meta'].fields)
    ALL = type(operationName, tuple(op_base_classes), properties)
    return ALL


def build_base_classes(operationName, operationModule, operationBase, clsName):
    class OperationAbstract(ObjectType):
        scopes = ['unauthorized']
        pass

    current_directory = os.path.dirname(os.path.abspath(__file__))
    current_module = current_directory.split('/')[-1]
    # subdirectories contient tous les répertoires de api_graphql (ou presque)
    subdirectories = [
        x for x in os.listdir(current_directory)
        if os.path.isdir(os.path.join(current_directory, x))
        and x != '__pycache__'
        and x != 'root'
        # ignore tests
        and x!= 'tests'
    ]
    op_base_classes = [OperationAbstract]

    for directory in subdirectories:
        try:
            # j'essaie d'importer le fichier api_graphql.nom_du_rep.operationModule
            module = importlib.import_module(
                '{0}.{1}.{2}'.format("api_graphql", directory, operationModule)
            )
            if module:
                classes = [x for x in getmembers(module, isclass)]
                opers = [x[1] for x in classes if clsName in x[0] and x[0] != operationBase]
                # opers contient toutes les classes du fichier query.py (s'il existe) à condition qu'elles aient un nom
                # qui contient clsname Et que leur nom ne soit pas operationBase
                op_base_classes += opers
            else:
                logger.info('wat?')
                logger.debug(current_directory)
        except ImportError: # ModuleNotFoundError?
            pass

    op_base_classes = op_base_classes[::-1]
    return op_base_classes
