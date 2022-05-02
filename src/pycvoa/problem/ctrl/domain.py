from pycvoa.problem.ctrl import DefinitionError
from pycvoa.problem.domain import Domain
from pycvoa.problem.types import *
import pycvoa.problem.ctrl.parameter as ctrl_param


def domain_layer_vector_list(layer_vector_variable, value_list: list, external_domain: Domain, internal_domain: Domain):
    current_domain = get_valid_domain(external_domain, internal_domain)
    __list_size(layer_vector_variable, value_list, current_domain)
    __layer_vector_list(layer_vector_variable, value_list, current_domain)


def __list_size(vector_variable, values, domain: Domain):
    if not domain.check_vector_size(vector_variable, values):
        raise ValueError("The size of " + str(values) + " is not compatible with the " + vector_variable
                         + " definition.")


def __layer_vector_list(layer_vector_variable, values, domain: Domain):
    for layer in values:
        for element, value in layer:
            element_definition = domain.get_component_element_definition(layer_vector_variable, element)
            if element_definition[0] is INTEGER:
                ctrl_param.is_int(value)
                if value < element_definition[1] or value > element_definition[2]:
                    raise ValueError(
                        "The " + element + " element of the " + str(values.index(layer)) + "-nh component "
                                                                                           "is not compatible with its definition.")
            elif element_definition[0] is REAL:
                ctrl_param.is_float(value)
                if value < element_definition[1] or value > element_definition[2]:
                    raise ValueError(
                        "The " + element + " element of the " + str(values.index(layer)) + "-nh component "
                                                                                           "is not compatible with its definition.")
            elif element_definition[0] is CATEGORICAL:
                ctrl_param.same_python_type(element_definition[1], value)
                if value not in element_definition[1]:
                    raise ValueError(
                        "The " + element + " element of the " + str(values.index(layer)) + "-nh component "
                                                                                           "is not compatible with its definition.")


def domain_basic_value(check_basic_variable, value, external_domain: Domain, internal_domain: Domain):
    valid_domain = get_valid_domain(external_domain, internal_domain)
    if not valid_domain.check_basic(check_basic_variable, value):
        raise ValueError("The value " + str(value) + " is not compatible with the "
                         + check_basic_variable + " variable definition.")


def domain_layer_element_value(layer_variable, element, value, external_domain: Domain, internal_domain: Domain):
    valid_domain = get_valid_domain(external_domain, internal_domain)
    if not valid_domain.check_element(layer_variable, element, value):
        raise ValueError(
            "The value " + str(
                value) + " is not valid for the " + element + " element in the " + layer_variable + " variable.")


def domain_basic_vector_list(check_basic_vector_variable, value_list: list, external_domain: Domain,
                             internal_domain: Domain):
    valid_domain = get_valid_domain(external_domain, internal_domain)
    res = valid_domain.check_vector_basic_values(check_basic_vector_variable, value_list)
    if res[0] != -1:
        raise ValueError("The " + res[0] + "-nh value must be " + res[1] + ".")


def domain_basic_vector_value(check_basic_vector_variable, value, external_domain: Domain, internal_domain: Domain):
    valid_domain = get_valid_domain(external_domain, internal_domain)
    if not valid_domain.check_vector_basic_value(check_basic_vector_variable, value):
        raise ValueError(
            "The value " + value + " is not valid for the " + check_basic_vector_variable + " variable.")


def domain_layer_vector_element(layer_vector_variable, element, value, external_domain: Domain,
                                internal_domain: Domain):
    valid_domain = get_valid_domain(external_domain, internal_domain)
    if not valid_domain.check_vector_layer_element_value(layer_vector_variable, element, value):
        raise ValueError(
            "The value " + value + " is not valid for the " + element + " element in the "
            + layer_vector_variable + "variable.")
    return valid_domain


def domain_layer_vector_component(layer_vector_variable, layer_values, external_domain: Domain,
                                  internal_domain: Domain):
    ctrl_param.is_dict(layer_values)
    valid_domain = get_valid_domain(external_domain, internal_domain)
    __check_component_type(layer_vector_variable, LAYER, valid_domain)
    for element, value in layer_values:
        element_definition = valid_domain.get_component_element_definition(layer_vector_variable, element)
        if element_definition[0] is INTEGER:
            ctrl_param.is_int(value)
            if value < element_definition[1] or value > element_definition[2]:
                raise ValueError("The " + element + " element is not compatible with its definition.")
        elif element_definition[0] is REAL:
            ctrl_param.is_float(value)
            if value < element_definition[1] or value > element_definition[2]:
                raise ValueError("The " + element + " element is not compatible with its definition.")
        elif element_definition[0] is CATEGORICAL:
            ctrl_param.same_python_type(element_definition[1], value)
            if value not in element_definition[1]:
                raise ValueError("The " + element + " element is not compatible with its definition.")


#######################################################################################################################
#######################################################################################################################


def get_valid_domain(external_domain: Domain, internal_domain: Domain) -> Domain:
    ctrl_param.is_domain_class(external_domain)
    current_domain = external_domain
    if current_domain is None:
        current_domain = internal_domain
    if current_domain is None:
        raise ValueError("A domain must be specified, via parameter or set_domain method.")
    return current_domain


def basic_variable(check_basic_variable, external_domain: Domain, internal_domain: Domain):
    valid_domain = get_valid_domain(external_domain, internal_domain)
    __check_variable_type(check_basic_variable, BASIC, valid_domain)
    return valid_domain


def layer_variable_element(check_layer_variable, element, external_domain, internal_domain):
    valid_domain = get_valid_domain(external_domain, internal_domain)
    __check_variable_type(check_layer_variable, LAYER, valid_domain)
    if valid_domain.is_defined_element(check_layer_variable, element) is not True:
        raise DefinitionError(
            "The element " + element + " of the " + check_layer_variable +
            " LAYER variable is not defined in this domain.")
    return valid_domain


def basic_vector_variable(check_vector_variable, external_domain, internal_domain):
    valid_domain = get_valid_domain(external_domain, internal_domain)
    __check_component_type(check_vector_variable, BASIC, valid_domain)
    return valid_domain


def __check_variable_type(variable, check_type, domain):
    var_type = domain.get_variable_type(variable)
    if check_type is BASIC:
        if var_type not in BASIC:
            raise ValueError("The " + variable + " variable is not defined as BASIC.")
    else:
        if var_type is not check_type:
            raise ValueError("The " + variable + " variable is not defined as " + check_type + ".")


def __check_component_type(check_vector_variable, check_type, domain):
    """ It checks if the components of a **VECTOR** variable are defined as a concrete type, if not, raise
    py:class:`~pycvoa.problem.domain.WrongItemType`.

    :param check_vector_variable: The **VECTOR** variable.
    :param check_type: The component type.
    :param domain: The domain
    :type check_vector_variable: str
    :type check_type: **INTEGER**, **REAL**, **CATEGORICAL**, **BASIC**, **LAYER**, **VECTOR**
    """
    comp_type = domain.get_vector_components_type(check_vector_variable)
    if check_type is BASIC:
        if comp_type not in BASIC:
            raise ValueError("The components of " + check_vector_variable + " are not defined as BASIC.")
    else:
        if comp_type is not check_type:
            raise ValueError("The components of " + check_vector_variable + " are not defined as " + check_type + ".")