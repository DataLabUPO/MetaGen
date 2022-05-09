from pycvoa.problem.ctrl import SolutionError
from pycvoa.problem.domain import Domain


def is_assigned_layer_element(layer_variable: str, element: str, solution_structure: dict):
    is_assigned_variable(layer_variable, solution_structure)
    if element not in solution_structure.get(layer_variable).keys():
        raise SolutionError(
            "The element " + element + " is not assigned in the " + layer_variable + " variable of this solution.")


def is_assigned_variable(variable, solution_structure: dict):
    if variable not in solution_structure.keys():
        raise SolutionError("The " + variable + " variable is not assigned in this solution.")


def is_assigned_component(vector_variable, index, solution_structure: dict):
    if index < 0 or index >= len(solution_structure.get(vector_variable)):
        raise SolutionError(
            "The " + str(
                index) + "-nh component of " + vector_variable + " VECTOR variable is not assigned in this solution.")


def is_assigned_component_element(layer_vector_variable: str, index: int, element, solution_structure: dict):
    if element not in solution_structure.get(layer_vector_variable)[index].keys():
        raise SolutionError("The element " + str(element) + " in not assigned in the " + str(index)
                            + "-nh component of the " + str(layer_vector_variable) + " variable in this solution.")


def vector_insertion_available(vector_variable: str, domain: Domain, solution_structure: dict):
    if vector_variable in solution_structure.keys():
        vector_size = len(solution_structure[vector_variable])
    else:
        vector_size = 0
    if domain.get_remaining_available_basic_components(vector_variable, vector_size) == 0:
        raise SolutionError("The " + str(vector_variable) + " is complete.")


def vector_adding_available(vector_variable: str, remaining: int):
    if remaining == 0:
        raise SolutionError("The " + str(vector_variable) + " is complete.")


def vector_element_adding_available(layer_vector_variable: str, solution_structure: dict, domain: Domain):
    pass


def assigned_vector_removal_available(vector_variable, solution_structure: dict, domain: Domain):
    is_assigned_variable(vector_variable, solution_structure)
    if domain.get_remaining_available_basic_components(vector_variable,
                                                       len(solution_structure.get(vector_variable))) < 0:
        raise SolutionError("The " + str(vector_variable) + " can not deleting.")
