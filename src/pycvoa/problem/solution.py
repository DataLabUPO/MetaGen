import copy
import sys
from pycvoa.problem.ctrl import parameter as ctrl_par
from pycvoa.problem.ctrl import solution as ctrl_sol
from pycvoa.problem.ctrl import domain as ctrl_dom
from pycvoa.problem.domain import Domain
from pycvoa.problem.types import *


class Solution:
    """ This class is an abstraction of a solution for a meta-heuristic that a third-party provides.

    The :py:class:`~pycvoa.cvoa.CVOA` algorithm uses this class to model the individuals in its emulated pandemic
    process.

    The default and unique, constructor builds an empty solution with the worst fitness value
    (:math:`best=False`, by default) or the best fitness value (:math:`best=False`). Furthermore, a
    :py:class:`~pycvoa.problem.domain.Domain` object can be passed to check the variable definitions internally and,
    therefore boost the Solution fucntionality.

    **Example:**

    .. code-block:: python

        >>> best_solution  = Solution(best=True)
        >>> best_solution.fitness
        0.0
        >>> worst_solution  = Solution()
        >>> worst_solution.fitness
        1.7976931348623157e+308
        >>> boosted_solution = Solution(domain=defined_domain)

    :param best: If true, build an individual with the best fitness value, defaults to True.
    :param domain: The domain of the solution, defaults to None.
    :type best: bool
    :type domain: :py:class:`~pycvoa.problem.domain.Domain`
    """

    def __init__(self, best=False, domain: OptDomain = None):
        """ It is the default and unique, constructor builds an empty solution with the worst fitness value
        (:math:`best=False`, by default) or the best fitness value (:math:`best=False`). Furthermore, a
        :py:class:`~pycvoa.problem.domain.Domain` object can be passed to check the variable definitions internally and,
        therefore boost the Solution fucntionality.

        :param best: If True the individual will be built with the best fitness function;
        otherwise the worst, defaults to False.
        :param domain: The domain of the solution, defaults to None.
        :ivar __domain: Domain associated with the solution.
        :ivar __variables: Data structure where the variables of a solution are stored.
        :ivar discovering_iteration_time: Pandemic time when a solution is discovered.
        :ivar fitness: Fitness value.
        :type best: bool
        :type domain: :py:class:`~pycvoa.problem.domain.Domain`
        :vartype __domain: :py:class:`~pycvoa.problem.domain.Domain`
        :vartype __variables: dict
        :vartype discovering_iteration_time: int
        :vartype fitness: float
        """
        self.__domain: OptDomain = domain
        self.__variables: VarStructureType = {}
        self.discovery_iteration: int = 0
        if best:
            self.fitness: float = 0.0
        else:
            self.fitness = sys.float_info.max

    # ** DOMAIN AVAILABILITY INTERFACE ***
    def set_domain(self, domain: Domain):
        """ It sets the domain of the solution.

        :param domain: The domain of the solution.
        :type domain: :py:class:`~pycvoa.problem.domain.Domain`
        """
        self.__domain = domain

    # ** BASIC TYPE METHODS ***
    def set_basic(self, basic_variable: str, value: BasicValue, domain: OptDomain = None):
        """ It sets the value of variable. If the variable does not exist, it will be created with the indicated value.

         **Precondition:**

        The queried variable must be **INTEGER**, **REAL** or **CATEGORICAL**. For **LAYER** and **VECTOR** variables,
        there are specific setters (:py:meth:`~pycvoa.individual.Individual.set_layer_element_value`,
        :py:meth:`~pycvoa.individual.Individual.set_vector_element_by_index` respectively and
        :py:meth:`~pycvoa.individual.Individual.set_vector_layer_element_by_index`)

        :param basic_variable: The name of the variable to set.
        :param value: The new value of the variable.
        :param domain: The domain used to check the type, defaults to None.
        :type basic_variable: str
        :type value: int, float, str
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.domain.NotDefinedVariable: The variable is not defined in this domain.
        :raise :py:class:`~pycvoa.problem.domain.WrongVariableType: The variable is not defined as **BASIC** type.
        :raise :py:class:`~pycvoa.problem.solution.WrongType: The variable is not defined as BASIC.
        :raise :py:class:`~pycvoa.problem.solution.WrongValue: The value is not valid.
        """
        ctrl_dom.check_basic_value(basic_variable, value, domain, self.__domain)
        self.__variables[basic_variable] = copy.deepcopy(value)

    # ** LAYER TYPE METHODS ***
    def set_layer(self, layer_variable: str, layer_value: LayerValue, domain: OptDomain = None):
        ctrl_dom.check_layer_value(layer_variable, layer_value, domain, self.__domain)
        self.__variables[layer_variable] = layer_value

    def set_element(self, layer_variable: str, element: str, value: BasicValue, domain: OptDomain = None):
        """ It sets the element value of a **LAYER** variable. If the **LAYER** variable does not exist,
        it will be created with the indicated value.

        :param layer_variable: The name of the variable to set.
        :param element: The new value of the variable.
        :param value: The new value of the variable.
        :param domain: The domain used to check the type, defaults to None.
        :type layer_variable: str
        :type element: str
        :type value: int, float, str
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.domain.NotDefinedVariable: The variable is not defined in the domain.
        :raise :py:class:`~pycvoa.problem.domain.WrongVariableType: The variable is not defined as **BASIC** type.
        :raise :py:class:`~pycvoa.problem.solution.WrongType: The variable is not defined as LAYER.
        :raise :py:class:`~pycvoa.problem.solution.WrongValue: The value is not valid.
        """
        ctrl_dom.check_layer_element_value(layer_variable, element, value, domain, self.__domain)
        if layer_variable not in self.__variables.keys():
            self.__variables[layer_variable] = {element: value}
        else:
            layer_value: OptValueTypes = self.__variables.get(layer_variable)
            assert type(layer_value) is dict
            layer_value[element] = value

    # ** BASIC VECTOR METHODS ***
    def set_basic_vector(self, vector_variable: str, values: BasicVectorValues, domain: OptDomain = None):
        ctrl_dom.check_basic_vector_values(vector_variable, values, domain, self.__domain)
        self.__variables[vector_variable] = copy.deepcopy(values)

    def add_basic_component(self, basic_vector_variable: str, value: BasicValue, domain: OptDomain = None) -> int:
        """ It appends a value at last of a **VECTOR** variable. If the **VECTOR** variable does not exist,
        it will be created with the indicated value in the 0 position.

        :param basic_vector_variable: The name of the variable to set.
        :param value: The new value.
        :param domain: The domain used to check the type, defaults to None.
        :type basic_vector_variable: str
        :type value: int, float, str, list
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.domain.NotDefinedVariable: The variable is not defined in this domain.
        :raise :py:class:`~pycvoa.problem.domain.WrongVariableType: The variable is not defined as **VECTOR**.
        :raise :py:class:`~pycvoa.problem.domain.WrongComponentType: The components of the **VECTOR** variable are not
        defined as a **BASIC** type.
        """
        return Solution.__put_basic(self.__variables, basic_vector_variable, value, domain, self.__domain)

    def insert_basic_component(self, basic_vector_variable: str, index: int, value: BasicValue,
                               domain: OptDomain = None) -> int:
        """ It inserts a value in the **index**-nh position of a **VECTOR** variable. If the **VECTOR** variable
        does not exist, it will be created with the indicated value in the 0 position.

        :param basic_vector_variable: The name of the variable to set.
        :param index: The index.
        :param value: The new value.
        :param domain: The domain used to check the type, defaults to None.
        :type basic_vector_variable: str
        :type index: int
        :type value: int, float, str, list
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.domain.NotDefinedVariable: The variable is not defined in this domain.
        :raise :py:class:`~pycvoa.problem.domain.WrongVariableType: The variable is not defined as **VECTOR**.
        :raise :py:class:`~pycvoa.problem.domain.WrongComponentType: The components of the **VECTOR** variable are not
        defined as a **BASIC** type.
        """
        return Solution.__put_basic(self.__variables, basic_vector_variable, value, domain, self.__domain, index)

    def set_basic_component(self, basic_vector_variable: str, index: int, value: BasicValue, domain: OptDomain = None):
        """ It sets **index**-nh position of a **VECTOR** variable. If the **VECTOR** variable does not exist,
        it will be created with the indicated value in the 0 position.

         **Precondition:**

        The type of the queried **VECTOR** variable must be **INTEGER**, **REAL** or **CATEGORICAL**.
        For **VECTOR** variables defined as **LAYER**, there is a specific setter
        (:py:meth:`~pycvoa.individual.Individual.set_vector_layer_element_by_index`)

        :param basic_vector_variable: The name of the variable to set.
        :param index: The position to set.
        :param value: The new value of the position.
        :param domain: The domain used to check the type, defaults to None.
        :type basic_vector_variable: str
        :type index: int
        :type value: int, float, str
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.solution.NotInSolutionError: The variable is not in this solution.
        :raise :py:class:`~pycvoa.problem.solution.WrongType: The variable is not defined as **VECTOR**.
        :raise :py:class:`~pycvoa.problem.domain.NotDefinedVariable: The variable is not defined in this domain.
        :raise :py:class:`~pycvoa.problem.domain.WrongComponentType: The components of the **VECTOR** variable are not
        defined as a **BASIC** type.
        :raise NotDefinedVectorComponentError: The **index**-nh component of the **VECTOR** variable is not available.
        :raise :py:class:`~pycvoa.problem.solution.WrongValue: The value is not valid.
        """
        ctrl_dom.check_basic_vector_value(basic_vector_variable, value, domain, self.__domain)
        if basic_vector_variable not in self.__variables.keys():
            self.__variables[basic_vector_variable] = [value]
        else:
            ctrl_sol.is_assigned_component(basic_vector_variable, index, self.__variables)
            self.__variables[basic_vector_variable][index] = value

    # ** LAYER VECTOR METHODS ***

    def set_layer_vector(self, layer_vector_variable: str, values: list[dict], domain: OptDomain = None):
        ctrl_dom.check_layer_vector_values(layer_vector_variable, values, domain, self.__domain)
        self.__variables[layer_vector_variable] = copy.deepcopy(values)

    # ++ COMPONENT LEVEL
    def add_layer_component(self, layer_vector_variable: str, layer_values: dict, domain: OptDomain = None) -> int:
        return Solution.__put_layer(self.__variables, layer_vector_variable, layer_values, domain, self.__domain)

    def insert_layer_component(self, layer_vector_variable: str, index: int, layer_values: dict,
                               domain: OptDomain = None) -> int:
        return Solution.__put_layer(self.__variables, layer_vector_variable, layer_values, domain, self.__domain, index)

    def set_layer_component(self, layer_vector_variable: str, index: int, layer_values: dict, domain: OptDomain = None):
        ctrl_dom.check_layer_vector_component(layer_vector_variable, layer_values, domain, self.__domain)
        if layer_vector_variable not in self.__variables.keys():
            self.__variables[layer_vector_variable] = [copy.deepcopy(layer_values)]
        else:
            ctrl_sol.is_assigned_component(layer_vector_variable, index, self.__variables)
            self.__variables[layer_vector_variable][index] = copy.deepcopy(layer_values)

    # ++ COMPONENT ELEMENT LEVEL
    def add_element_to_layer_component(self, layer_vector_variable: str, element: str, value: BasicValue,
                                       domain: OptDomain = None) -> list:
        """ It appends a value at last of a **VECTOR** variable. If the **VECTOR** variable does not exist,
        it will be created with the indicated value in the 0 position.

        :param layer_vector_variable: The name of the variable to set.
        :param value: The new value.
        :param element: The element.
        :param domain: The domain used to check the type, defaults to None.
        :type layer_vector_variable: str
        :type value: int, float, str, list
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.domain.NotDefinedVariable: The variable is not defined in this domain.
        :raise :py:class:`~pycvoa.problem.domain.WrongVariableType: The variable is not defined as **VECTOR**.
        :raise :py:class:`~pycvoa.problem.domain.WrongComponentType: The components of the **VECTOR** variable are not
        defined as a **BASIC** type.
        """
        return Solution.__put_element(self.__variables, layer_vector_variable, element, value,
                                      domain, self.__domain)

    def insert_element_to_layer_component(self, layer_vector_variable: str, index: int, element: str, value: BasicValue,
                                          domain: OptDomain = None) -> list:
        """ It inserts a value in the **index**-nh position of a **VECTOR** variable. If the **VECTOR** variable
        does not exist, it will be created with the indicated value in the 0 position.

        :param layer_vector_variable: The name of the variable to set.
        :param index: The index.
        :param element: The element.
        :param value: The new value.
        :param domain: The domain used to check the type, defaults to None.
        :type layer_vector_variable: str
        :type index: int
        :type value: int, float, str, list
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.domain.NotDefinedVariable: The variable is not defined in this domain.
        :raise :py:class:`~pycvoa.problem.domain.WrongVariableType: The variable is not defined as **VECTOR**.
        :raise :py:class:`~pycvoa.problem.domain.WrongComponentType: The components of the **VECTOR** variable are not
        defined as a **BASIC** type.
        """
        return Solution.__put_element(self.__variables, layer_vector_variable, element, value, domain,
                                      self.__domain, index)

    def set_element_of_layer_component(self, layer_vector_variable: str, index: int, element: str, value: BasicValue,
                                       domain: OptDomain = None):
        """ It sets an element of a **LAYER** in the **index**-nh position of a **VECTOR** variable.

        :param layer_vector_variable: The name of the variable to set.
        :param index: The position to set.
        :param element: The layer element name.
        :param value: The new value of the layer element.
        :param domain: The domain used to check the type, defaults to None.
        :type layer_vector_variable: str
        :type index: int
        :type element: str
        :type value: int, float, str
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.solution.NotInSolutionError: The variable is not in this solution.
        :raise :py:class:`~pycvoa.problem.solution.WrongType: The variable is not defined as **VECTOR**.
        :raise :py:class:`~pycvoa.problem.domain.NotDefinedVariable: The variable is not defined in this domain.
        :raise :py:class:`~pycvoa.problem.domain.WrongComponentType: The components of the VECTOR variable are not
        defined as LAYER.
        :raise :py:class:`~pycvoa.problem.solution.NotDefinedVectorComponentError: The **index**-nh component of the
        **VECTOR** variable is not available.
        :raise :py:class:`~pycvoa.problem.solution.WrongValue: The value is not valid.
        """
        ctrl_dom.check_layer_vector_element(layer_vector_variable, element, value, domain, self.__domain)
        if layer_vector_variable not in self.__variables.keys():
            self.__variables[layer_vector_variable] = [{element: value}]
        else:
            ctrl_sol.is_assigned_component(layer_vector_variable, index, self.__variables)
            self.__variables[layer_vector_variable][index][element] = value

    # ** SET VALUE METHOD

    def set_value(self, variable: str, value: AllValues, index: OptInt = None, element: OptStr = None,
                  domain: OptDomain = None):
        """ It sets a value of a variable.

             This member has three use cases:

             - BASIC TYPE: Only the variable name must be provided.
             - LAYER TYPE: The variable type and the element name must be provided.
             - VECTOR TYPE: The variable name and the index of the component must be provided.
                 - If the components are defined as a LAYER TYPE: The element must be also provided.

        :param variable: The variable name.
        :param value: The new value.
        :param index: Index position of a **VECTOR** variable, defaults to None.
        :param element: Element of a **LAYER** variable, defaults to None.
        :param domain: The domain used to check the type, defaults to None.
        :type variable: str
        :type index: int
        :type element: str
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.domain.NotDefinedVariable: The variable is not defined in this domain.
        :raise :py:class:`~pycvoa.problem.solution.WrongParameters: Index/element parameter must be provided.
        :raise :py:class:`~pycvoa.problem.domain.WrongVariableType: The variable is not defined as **BASIC**/**VECTOR**
        type.
        :raise :py:class:`~pycvoa.problem.solution.WrongType: The variable is not defined as BASIC/LAYER/VECTOR.
        :raise :py:class:`~pycvoa.problem.solution.WrongValue: The value is not valid.
        :raise :py:class:`~pycvoa.problem.solution.NotInSolutionError: The variable is not in this solution.
        :raise :py:class:`~pycvoa.problem.domain.WrongComponentType: The components of the **VECTOR** variable are not
        defined as a **BASIC**/**LAYER** type.
        :raise NotDefinedVectorComponentError: The **index**-nh component of the **VECTOR** variable is not available.
        :raise :py:class:`~pycvoa.problem.solution.WrongValue: The value is not valid.
        """
        current_domain = ctrl_dom.get_valid_domain(domain, self.__domain)
        var_type = current_domain.get_variable_type(variable)
        if var_type in BASIC_TYPE:
            assert index is None
            assert element is None
            self.set_basic(variable, value, current_domain)
        elif var_type is LAYER_TYPE:
            assert index is None
            assert element is not None
            self.set_element(variable, element, value, current_domain)
        elif var_type is VECTOR_TYPE:
            assert index is not None
            vector_definition = current_domain.get_vector_component_definition(variable)
            if vector_definition in BASIC_TYPE:
                assert element is None
                self.set_basic_component(variable, index, value, current_domain)
            elif vector_definition is LAYER_TYPE:
                assert element is not None
                self.set_element_of_layer_component(variable, index, element, value, current_domain)

    # ** VECTOR REMOVES ***

    def remove_component(self, vector_variable: str, domain: OptDomain = None):
        """ It removes the last position of a **VECTOR** variable.

        :param vector_variable: The name of the **VECTOR** variable to modify.
        :param domain: The domain used to check the type, defaults to None.
        :type vector_variable: str
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.solution.NotInSolutionError: The variable is not in this solution.
        :raise :py:class:`~pycvoa.problem.solution.WrongType: The variable is not defined as VECTOR.
        """
        valid_domain = ctrl_dom.get_valid_domain(domain, self.__domain)
        ctrl_sol.is_assigned_variable(vector_variable, self.__variables)
        r = ctrl_sol.assigned_vector_removal_available(vector_variable, self.__variables, valid_domain)
        self.__variables[vector_variable].pop()
        return r

    def delete_component(self, vector_variable: str, index: int, domain: OptDomain = None):
        """ It removes a value in the **index**-nh position of a **VECTOR** variable.

        :param vector_variable: The name of the **VECTOR** variable to modify.
        :param index: The index.
        :param domain: The domain used to check the type, defaults to None.
        :type vector_variable: str
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.solution.NotInSolutionError: The variable is not in this solution.
        :raise :py:class:`~pycvoa.problem.solution.WrongType: The variable is not defined as **VECTOR**.
        :raise :py:class:`~pycvoa.problem.solution.NotDefinedVectorComponentError: The **index**-nh component of the
        **VECTOR** variable is not available.
        """
        valid_domain = ctrl_dom.get_valid_domain(domain, self.__domain)
        ctrl_sol.is_assigned_variable(vector_variable, self.__variables)
        r = ctrl_sol.assigned_vector_removal_available(vector_variable, self.__variables, valid_domain)
        ctrl_sol.is_assigned_component(vector_variable, index, self.__variables)
        del self.__variables[vector_variable][index]
        return r

    # ** IS METHODS ***

    def is_available(self, variable: str) -> bool:
        """ It checks if the input variable has a value in this solution.

        :param variable: The variable to check.
        :returns: True if the variable has a value, otherwise False.
        :type variable: str
        :rtype: bool
        """
        r = False
        if variable in self.__variables.keys():
            r = True
        return r

    def check_variable_type(self, variable: str, check_type: str, domain: OptDomain = None) -> bool:
        """ It checks if the input variable is equal to the input variable type, taking into account the internal
        solution domain (by default) or a domain passed as parameter.

        :param variable: The variable to check.
        :param check_type: The variable type to check.
        :param domain: The domain used to check the type, defaults to None.
        :returns: True if the variable is defined as the queried variable type, otherwise False
        :type variable: str
        :type check_type: INTEGER, REAL, CATEGORICAL, LAYER, VECTOR
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :rtype: bool
        :raise :py:class:`~pycvoa.problem.solution.DomainLevel: The domain is not set.
        :raise :py:class:`~pycvoa.problem.solution.NotInSolutionError: The variable is not in this solution.
        :raise :py:class:`~pycvoa.problem.domain.NotDefinedVariable: The variable is not defined in this domain.
        """
        valid_domain = ctrl_dom.domain_defined_assigned(variable, self.__variables, domain, self.__domain)
        variable_type = valid_domain.get_variable_type(variable)
        r = False
        if check_type is BASIC_TYPE:
            if variable_type in BASIC_TYPE:
                r = True
        else:
            if variable_type is check_type:
                r = True
        return r

    def check_component_type(self, vector_variable: str, check_component_type: str, domain: OptDomain = None) -> bool:
        """ It checks if the components of the input variable (defined as **VECTOR**) is equal to the input component
        type, taking into account the internal solution domain (by default) or a domain passed as parameter.

        :param vector_variable: The **VECTOR** variable to check.
        :param check_component_type: The component type to check.
        :param domain: The domain used to check the type, defaults to None.
        :returns: True if the variable is defined as the queried variable type, otherwise False
        :type vector_variable: str
        :type check_component_type: INTEGER, REAL, CATEGORICAL, LAYER, VECTOR
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :rtype: bool
        :raise :py:class:`~pycvoa.problem.solution.DomainLevel: The domain is not set.
        :raise :py:class:`~pycvoa.problem.solution.NotInSolutionError: The variable is not in this solution.
        :raise :py:class:`~pycvoa.problem.domain.NotDefinedVariable: The variable is not defined in this domain.
        :raise :py:class:`~pycvoa.problem.domain.WrongVariableType: The variable is not defined as **VECTOR**.
        """
        valid_domain = ctrl_dom.domain_defined_as_vector_assigned(vector_variable, self.__variables, domain,
                                                                  self.__domain)
        component_type = valid_domain.get_vector_components_type(vector_variable)
        r = False
        if check_component_type is BASIC_TYPE:
            if component_type in BASIC_TYPE:
                r = True
        else:
            if component_type is check_component_type:
                r = True
        return r

    def is_available_element(self, layer_variable: str, element: str, domain: OptDomain = None) -> bool:
        """ It checks if the input element of the input **LAYER** variable has a value in this solution, taking into
        account the internal solution domain (by default) or a domain passed as parameter.

        :param layer_variable: The **LAYER** variable to check.
        :param element: The element to check.
        :param domain: The domain used to check the type, defaults to None.
        :returns: True if the element has a value, otherwise False.
        :type layer_variable: str
        :type element: str
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :rtype: bool
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.solution.NotInSolutionError: The variable is not in this solution.
        :raise :py:class:`~pycvoa.problem.solution.WrongType: The variable is not defined as **LAYER**.
        """
        ctrl_dom.domain_defined_as_layer_assigned(layer_variable, self.__variables, domain, self.__domain)
        r = False
        if element in self.__variables.get(layer_variable).keys():
            r = True
        return r

    def is_available_component(self, vector_variable: str, index: int, domain: OptDomain = None) -> bool:
        """ It checks if the *index*-nh component of the input **VECTOR** variable has a value in this solution,
        taking into account the internal solution domain (by default) or a domain passed as parameter.

        :param vector_variable: The **VECTOR** variable to check.
        :param index: The index of the component to check.
        :param domain: The domain used to check the type, defaults to None.
        :returns: True if the *index*-nh component has a value, otherwise False.
        :type vector_variable: str
        :type index: int
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :rtype: bool
        :raise :py:class:`~pycvoa.problem.solution.DomainLevel: The domain is not set.
        :raise :py:class:`~pycvoa.problem.solution.NotInSolutionError: The variable is not in this solution.
        :raise :py:class:`~pycvoa.problem.solution.WrongType: The variable is not defined as **VECTOR**.
        """
        ctrl_dom.domain_defined_as_vector_assigned(vector_variable, self.__variables, domain, self.__domain)
        r = False
        if 0 <= index < len(self.__variables.get(vector_variable)):
            r = True
        return r

    def is_available_component_element(self, layer_vector_variable: str, index: int, element: str,
                                       domain: OptDomain = None):
        """ It checks if the input element of the *index*-nh component (defined as **LAYER**) of the input **VECTOR**
        variable has a value in this solution, taking into account the internal solution domain (by default) or
        a domain passed as parameter.

        :param layer_vector_variable: The **VECTOR** variable to check.
        :param index: The index of the component to check.
        :param element: The element to check.
        :param domain: The domain used to check the type, defaults to None.
        :returns: True if the *index*-nh component has a value, otherwise False.
        :type layer_vector_variable: str
        :type index: int
        :type element: str
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :rtype: bool
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.solution.NotInSolutionError: The variable is not in this solution.
        :raise :py:class:`~pycvoa.problem.solution.WrongType: The variable is not defined as **VECTOR**.
        :raise :py:class:`~pycvoa.problem.domain.NotDefinedVariable: The variable is not defined in the domain.
        :raise :py:class:`~pycvoa.problem.solution.WrongComponentType: The component type is not defined as **LAYER**.
        :raise :py:class:`~pycvoa.problem.solution.NotDefinedVectorComponentError: The component is not available.
        """
        ctrl_dom.domain_defined_as_layer_vector_assigned(layer_vector_variable, self.__variables, domain,
                                                         self.__domain)
        ctrl_sol.is_assigned_component(layer_vector_variable, index, self.__variables)
        r = False
        if element in self.__variables.get(layer_vector_variable)[index].keys():
            r = True
        return r

    # ** GETTERS ***
    def get_basic_value(self, basic_variable: str, domain: OptDomain = None):
        """ It returns a variable value of a **BASIC** variable of the solution.

        **Precondition:**

        The queried variable must be **INTEGER**, **REAL** or **CATEGORICAL**.

        For **LAYER** and **VECTOR** variables, there are specific getters:

        - :py:meth:`~pycvoa.problem.solution.Solution.get_element_value`,
        - :py:meth:`~pycvoa.problem.solution.Solution.get_component_value`
        - :py:meth:`~pycvoa.problem.solution.Solution.get_component_element_value`

        :param basic_variable: The variable.
        :param domain: The domain used to check the type, defaults to None.
        :returns: The variable value.
        :type basic_variable: str
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :rtype: int, float, str
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.solution.NotInSolutionError: The variable is not in this solution.
        :raise :py:class:`~pycvoa.problem.solution.WrongType: The variable is not defined as BASIC.
        """
        ctrl_dom.basic_variable(basic_variable, domain, self.__domain)
        ctrl_sol.is_assigned_variable(basic_variable, self.__variables)
        return self.__variables.get(basic_variable)

    def get_element_value(self, layer_variable: str, element: str, domain: OptDomain = None):
        """ It returns an element value of a **LAYER** variable of the solution.

        :param layer_variable: The **LAYER** variable.
        :param element: The element.
        :param domain: The domain used to check the type, defaults to None.
        :returns: The element value of the **LAYER** variable.
        :type layer_variable: str
        :type element: str
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :rtype: int, float, str
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.solution.NotInSolutionError: The variable is not in this solution.
        :raise :py:class:`~pycvoa.problem.solution.WrongType: The variable is not defined as **LAYER**.
        :raise :py:class:`~pycvoa.problem.solution.NotDefinedLayerElementError: The element is not defined in the
        **LAYER** variable.
        """
        ctrl_dom.layer_variable_element(layer_variable, self.__variables, domain, self.__domain)
        ctrl_sol.is_assigned_layer_element(layer_variable, element, self.__variables)
        return self.__variables.get(layer_variable).get(element)

    def get_basic_component_value(self, basic_vector_variable: str, index: int, domain: OptDomain = None):
        """ It returns the **index**-nh value of a **VECTOR** variable defined as **BASIC** of the solution.

        :param basic_vector_variable: The variable.
        :param index: The index of the element to get.
        :param domain: The domain used to check the type, defaults to None.
        :returns: The **index**-nh value of the size **VECTOR** variable.
        :type basic_vector_variable: str
        :type index: int
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :rtype: float, int, str
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.solution.NotInSolutionError: The variable is not in this solution.
        :raise :py:class:`~pycvoa.problem.solution.WrongType: The variable is not defined as **VECTOR**.
        :raise :py:class:`~pycvoa.problem.domain.NotDefinedVariable: The variable is not defined in the domain.
        :raise :py:class:`~pycvoa.problem.solution.WrongComponentType: The components of the **VECTOR** variable is not
        defined as **BASIC**.
        :raise :py:class:`~pycvoa.problem.solution.NotDefinedVectorComponentError: The **index**-nh component of the
        **VECTOR** variable is not available.
        """
        ctrl_par.is_int("index", index)
        ctrl_dom.basic_vector_variable(basic_vector_variable, domain, self.__domain)
        ctrl_sol.is_assigned_component(basic_vector_variable, index, self.__variables)
        return self.__variables.get(basic_vector_variable)[index]

    def get_layer_component_value(self, layer_vector_variable: str, index: int, element: str, domain: OptDomain = None):
        """ It returns a **LAYER** element value of the **index**-nh component of a **VECTOR** variable
        of the solution.

        :param layer_vector_variable: The variable.
        :param index: The index of the element to get.
        :param element: The element.
        :param domain: The domain used to check the type, defaults to None.
        :returns: The element value of the **index**-nh position of the **VECTOR** variable.
        :type layer_vector_variable: str
        :type index: int
        :type element: str
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :rtype: float, int, str
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.solution.NotInSolutionError: The variable is not in this solution.
        :raise :py:class:`~pycvoa.problem.solution.WrongType: The variable is not defined as **VECTOR**.
        :raise :py:class:`~pycvoa.problem.domain.NotDefinedVariable: The variable is not defined in the domain.
        :raise :py:class:`~pycvoa.problem.solution.WrongComponentType: The component type is not defined as **LAYER**.
        :raise :py:class:`~pycvoa.problem.solution.NotDefinedComponentElementError: The element of the **index**-nh
        component of the **VECTOR** variable is not available.
        """
        ctrl_par.is_int("index", index)
        ctrl_par.is_string("element", element)
        ctrl_dom.layer_vector(layer_vector_variable, domain, self.__domain)
        ctrl_sol.is_assigned_component_element(layer_vector_variable, index, element, self.__variables)
        return self.__variables.get(layer_vector_variable)[index][element]

    def get_value(self, variable: str, index: OptInt = None, element: OptStr = None, domain: OptDomain = None):
        """ It returns a value of a variable.

        This member has three use cases:

        - BASIC TYPE: Only the **BASIC** variable must be provided.
        - LAYER TYPE: A **LAYER** variable and the element name must be provided.
        - VECTOR TYPE: A **VECTOR** variable and the index of the component must be provided. If the components are
        defined as **LAYER**, the element must be also provided.

        :param variable: The variable.
        :param index: The index of a position of a **VECTOR** variable, defaults to None.
        :param element: The element of a **LAYER** variable, defaults to None.
        :param domain: The domain used to check the type, defaults to None.
        :returns: The value.
        :type variable: str
        :type index: int
        :type element: str
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :rtype: int, float, str
        :raise :py:class:`~pycvoa.problem.domain.NotDefinedVariable: The variable is not defined in the domain.
        :raise :py:class:`~pycvoa.problem.solution.NotInSolutionError: The variable is not in this solution.
        :raise :py:class:`~pycvoa.problem.solution.WrongType: The variable is not defined as BASIC.
        The variable is not defined as **VECTOR**.
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.solution.WrongParameters: The element of a **LAYER** variable is not provided.
        The index of a component of a **VECTOR** variable is not provided. The element of component of a **VECTOR**
        variable defined as **LAYER** is not provided.
        :raise :py:class:`~pycvoa.problem.solution.WrongType: The variable is not defined as **LAYER**.
        :raise :py:class:`~pycvoa.problem.solution.NotDefinedLayerElementError: The element is not defined in the
        **LAYER** variable.
        :raise :py:class:`~pycvoa.problem.domain.WrongVariableType: The variable is not defined as **VECTOR**.
        :raise :py:class:`~pycvoa.problem.solution.WrongComponentType: The components of the **VECTOR** variable is not
        defined as **BASIC**. The component type is not defined as **LAYER**.
        :raise :py:class:`~pycvoa.problem.solution.NotDefinedVectorComponentError: The **index**-nh component of the
        **VECTOR** variable is not available.
        """
        current_domain = ctrl_dom.get_valid_domain(domain, self.__domain)
        var_type = current_domain.get_variable_type(variable)
        r = None
        if var_type in BASIC_TYPE:
            assert index is None
            assert element is None
            r = self.get_basic_value(variable, current_domain)
        elif var_type is LAYER_TYPE:
            assert index is None
            assert element is not None
            r = self.get_element_value(variable, element, current_domain)
        elif var_type is VECTOR_TYPE:
            assert index is not None
            vector_definition = current_domain.get_vector_component_definition(variable)
            if vector_definition in BASIC_TYPE:
                assert element is None
                r = self.get_basic_component_value(variable, index, current_domain)
            elif vector_definition is LAYER_TYPE:
                assert element is not None
                r = self.get_layer_component_value(variable, index, element, current_domain)
        return r

    def get_vector_size(self, vector_variable: str, domain: OptDomain = None):
        """ It returns the size of a **VECTOR** variable of the solution. It is useful to access the values
        of the **VECTOR** variable sequentially.

        :param vector_variable: The **VECTOR** variable name.
        :param domain: The domain used to check the type, defaults to None.
        :returns: The size of the **VECTOR** variable.
        :type vector_variable: str
        :type domain: :py:class:`~pycvoa.problem.domain.Domain
        :rtype: int
        :raise :py:class:`~pycvoa.problem.solution.NotSpecifiedDomain: The domain is not set.
        :raise :py:class:`~pycvoa.problem.solution.WrongType: The variable is not defined as **VECTOR**.
        :raise :py:class:`~pycvoa.problem.solution.NotInSolutionError: The variable is not in this solution.
        """
        ctrl_dom.vector_type(vector_variable, domain, self.__domain)
        ctrl_sol.is_assigned_variable(vector_variable, self.__variables)
        return len(self.__variables.get(vector_variable))

    # ** STATICS METHODS **

    @staticmethod
    def __put_basic(variables: dict,
                    basic_vector_variable: str, value: BasicValue,
                    external_domain: OptDomain, internal_domain: OptDomain,
                    index: OptInt = None):
        valid_domain = ctrl_dom.check_basic_vector_value(basic_vector_variable, value, external_domain, internal_domain)
        if basic_vector_variable not in variables:
            variables[basic_vector_variable] = [value]
            r = valid_domain.get_remaining_available_complete_components(basic_vector_variable,
                                                                         len(variables[basic_vector_variable]))
        else:
            ctrl_sol.vector_insertion_available(basic_vector_variable, valid_domain, variables)
            r = valid_domain.get_remaining_available_complete_components(basic_vector_variable,
                                                                         len(variables[basic_vector_variable]))
            ctrl_sol.vector_adding_available(basic_vector_variable, r)
            if index is None:
                variables[basic_vector_variable].append(value)
            else:
                variables[basic_vector_variable].insert(index, value)
            r -= 1
        return r

    @staticmethod
    def __put_layer(variables: dict, layer_vector_variable: str, layer_values: dict,
                    external_domain: OptDomain, internal_domain: OptDomain,
                    index: OptInt = None):
        current_domain = ctrl_dom.check_layer_vector_component(layer_vector_variable, layer_values,
                                                               external_domain, internal_domain)
        if layer_vector_variable not in variables.keys():
            variables[layer_vector_variable] = [copy.deepcopy(layer_values)]
            r = current_domain.get_remaining_available_complete_components(layer_vector_variable,
                                                                           len(variables[layer_vector_variable]))
        else:
            r = current_domain.get_remaining_available_complete_components(layer_vector_variable,
                                                                           len(variables[layer_vector_variable]))
            ctrl_sol.vector_adding_available(layer_vector_variable, r)
            if index is None:
                variables[layer_vector_variable].append(copy.deepcopy(layer_values))
            else:
                variables[layer_vector_variable].insert(index, layer_values)
            r -= 1
        return r

    @staticmethod
    def __put_element(variables: dict,
                      layer_vector_variable: str, element: str, value: BasicValue,
                      external_domain: OptDomain, internal_domain: OptDomain,
                      index: OptInt = None) -> list:
        valid_domain = ctrl_dom.check_layer_vector_element(layer_vector_variable, element, value, external_domain,
                                                           internal_domain)
        if layer_vector_variable not in variables.keys():
            variables[layer_vector_variable] = [{element: value}]
        else:
            ctrl_sol.vector_element_adding_available(layer_vector_variable, variables, valid_domain)
            if index is None:
                valid_index = -1
            else:
                ctrl_par.is_int("index", index)
                valid_index = index

            if element in variables[layer_vector_variable][valid_index].keys():
                if index is None:
                    variables[layer_vector_variable].append({element: value})
                else:
                    variables[layer_vector_variable].insert(index, {element: value})
            else:
                variables[layer_vector_variable][valid_index][element] = value

        return valid_domain.get_remaining_available_layer_components(layer_vector_variable,
                                                                     len(variables[layer_vector_variable]),
                                                                     variables[layer_vector_variable][valid_index])

    # ** TO STRING **

    def __str__(self):
        """ String representation of a :py:class:`~pycvoa.individual.Individual` object
        """
        res = "F = " + str(self.fitness) + "\t{"
        count = 1
        for variable in sorted(self.__variables):
            res += str(variable) + " = " + str(self.__variables[variable])
            if count < len(self.__variables):
                res += " , "
            count += 1
        res += "}"
        return res

    # ** SET INTERNAL METHODS **

    def __eq__(self, other):
        """ Equity function of the :py:class:`~pycvoa.individual.Individual` class. An
        :py:class:`~pycvoa.individual.Individual` object is equal to another :py:class:`~pycvoa.individual.Individual`
        object if they have the same variables with the same values.
        """
        res = True

        if not isinstance(other, Solution):
            res = False
        else:
            i = 0
            keys = list(self.__variables.keys())
            while i < len(keys) & res:
                vf = self.get_basic_value(keys[i])
                vo = other.get_basic_value(keys[i])
                if vf != vo:
                    res = False
                i += 1

        return res

    def __ne__(self, other):
        """ Non Equity function of the :py:class:`~pycvoa.individual.Individual` class. An
        :py:class:`~pycvoa.individual.Individual` object is not equal to another :
        py:class:`~pycvoa.individual.Individual` object if they do not have the same variables with the same values.
        """
        return not self.__eq__(other)

    def __hash__(self):
        """ Hash function for :py:class:`~pycvoa.individual.Individual` objects. It is necessary for set structure
        management.
        """
        return hash((self.__variables.__hash__, self.fitness))

    def __lt__(self, other):
        """ *Less than* function for :py:class:`~pycvoa.individual.Individual` objects. An individual **A** is less
        than another individual **B** if the fitness value of **A** is strictly less than the fitness value of **B**.
        It is necessary for set structure management.
        """
        return self.fitness < other.fitness

    def __le__(self, other):
        """ *Less equal* function for :py:class:`~pycvoa.individual.Individual` objects. An individual **A** is less or
        equal than another individual **B** if the fitness value of **A** is less or equal than the fitness value
        of **B**. It is necessary for set structure management.
        """
        return self.fitness <= other.fitness

    def __gt__(self, other):
        """ *Greater than* function for :py:class:`~pycvoa.individual.Individual` objects. An individual **A** is
        greater than another individual **B** if the fitness value of **A** strictly greater than the fitness value
        of **B**. It is necessary for set structure management.
        """
        return self.fitness > other.fitness

    def __ge__(self, other):
        """ *Greater equal* function for :py:class:`~pycvoa.individual.Individual` objects. An individual **A** is
        greater or equal than another individual **B** if the fitness value of **A** greater or equal than the
        fitness value of **B**. It is necessary for set structure management.
        """
        return self.fitness >= other.fitness
