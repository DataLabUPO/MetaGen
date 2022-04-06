from pycvoa import INTEGER, REAL, CATEGORICAL, LAYER, VECTOR
from pycvoa.support import variable_definition_to_string


class ProblemDefinition:
    """ This class provides the required functionality to define a problem. The user must instantiate the class into a
    variable and, next, define the problem variables using the member methods of the class.

    **Example:**

    .. code-block:: python

        problem_definition = ProblemDefinition()
        problem_definition.register_categorical_variable("Categorical",["C1","C2","C3"])
    """

    def __init__(self):
        """ It is the default, and unique, constructor without parameters.

        :ivar __definitions: Data structure where the Problem Definition is stored.
        :vartype __definitions: dict
        """
        self.__definitions = {}

    def register_integer_variable(self, name, min_value, max_value, step):
        """ It defines an integer variable receiving the variable name, the minimum and maximum values that it will
        be able to have, and the step size to traverse the interval.

        :param name: Variable name.
        :param min_value: Minimum value
        :param max_value: Maximum value
        :param step: Step size
        :type name: str
        :type min_value: int
        :type max_value: int
        :type step: int
        """
        self.__definitions[name] = [INTEGER, min_value, max_value, step]

    def register_real_variable(self, name, min_value, max_value, step):
        """ It defines a real variable receiving the variable name, the minimum and maximum values that it will be
        able to have, and the step size to traverse the interval.

        :param name: Variable name.
        :param min_value: Minimum value.
        :param max_value: Maximum value.
        :param step: Step size.
        :type name: str
        :type min_value: float
        :type max_value: float
        :type step: float
        """
        self.__definitions[name] = [REAL, min_value, max_value, step]

    def register_categorical_variable(self, name, categories):
        """ It defines a categorical variable receiving the variable name, and a list with the labels that it will be
        able to have.

        :param name: Variable name.
        :param categories: List of labels.
        :type name: str
        :type categories: list
        """
        self.__definitions[name] = [CATEGORICAL, categories]

    def register_layer_variable(self, name):
        """ It defines a layer variable receiving the variable name. Next, the layer elements have to be defined using
        the methods:

        - :py:meth:`~pycvoa.definition.ProblemDefinition.insert_layer_integer`
        - :py:meth:`~pycvoa.definition.ProblemDefinition.insert_layer_real`
        - :py:meth:`~pycvoa.definition.ProblemDefinition.insert_layer_categorical`

        :param name: Variable name.
        :type name: str
        """
        self.__definitions[name] = [LAYER, {}]

    def insert_layer_integer(self, layer_name, element_name, min_value, max_value, step):
        """ It inserts an integer element into the layer_name variable by receiving the element name, the minimum and
        maximum values that it will be able to have, and the step size to traverse the interval.

        :param layer_name: Layer variable where the new element will be inserted.
        :param element_name: Element name.
        :param min_value: Minimum value.
        :param max_value: Maximum value.
        :param step: Step size.
        :type layer_name: str
        :type element_name: str
        :type min_value: int
        :type max_value: int
        :type step: int
        """
        layer_elements = self.__definitions[layer_name][1]
        layer_elements[element_name] = [INTEGER, min_value, max_value, step]

    def insert_layer_real(self, layer_name, element_name, min_value, max_value, step):
        """ It inserts a real element into the layer_name variable by receiving the element name, the minimum and
        maximum values that it will be able to have, and the step size to traverse the interval.

        :param layer_name: Layer variable where the new element will be inserted.
        :param element_name: Element name.
        :param min_value: Minimum value.
        :param max_value: Maximum value.
        :param step: Step size.
        :type layer_name: str
        :type element_name: str
        :type min_value: float
        :type max_value: float
        :type step: float
        """
        layer_elements = self.__definitions[layer_name][1]
        layer_elements[element_name] = [REAL, min_value, max_value, step]

    def insert_layer_categorical(self, layer_name, element_name, categories):
        """ It inserts a categorical element into the layer_name variable by receiving the element name, and a list with
        the labels that it will be able to have.

        :param layer_name: Layer variable where the new element will be inserted.
        :param element_name: Element name.
        :param categories: List of labels.
        :type layer_name: str
        :type element_name: str
        :type categories: list
        """
        layer_elements = self.__definitions[layer_name][1]
        layer_elements[element_name] = [CATEGORICAL, categories]

    def register_vector_variable(self, name, min_size, max_size, step_size):
        """ It defines a vector variable receiving the variable name, the minimum and maximum size that it will be able
        to have, and the step size to select the size from the :math:`[min\_size, max\_size]`. Afterwards, the vector
        type must be set using the following methods:

        - :py:meth:`~definition.ProblemDefinition.set_vector_component_to_integer`
        - :py:meth:`~definition.ProblemDefinition.set_vector_component_to_real`
        - :py:meth:`~definition.ProblemDefinition.set_vector_component_to_categorical`
        - :py:meth:`~definition.ProblemDefinition.set_vector_component_to_layer`

        :param name: Variable name.
        :param min_size: Minimum size.
        :param max_size: Maximum size.
        :param step_size: Step size.
        :type name: str
        :type min_size: int
        :type max_size: int
        :type step_size: int
        """
        self.__definitions[name] = [VECTOR, min_size, max_size, step_size, {}]

    def set_vector_component_to_integer(self, vector_variable_name, min_value, max_value, step):
        """ It set the component type of the vector variable to integer by receiving the minimum and
        maximum values that it will be able to have, and the step size to traverse the interval

        :param vector_variable_name: Vector variable name previously defined.
        :param min_value: Minimum value.
        :param max_value: Maximum value.
        :param step: Step size.
        :type vector_variable_name: str
        :type min_value: int
        :type max_value: int
        :type step: int
        """
        self.__definitions[vector_variable_name][4] = [INTEGER, min_value, max_value, step]

    def set_vector_component_to_real(self, vector_variable_name, min_value, max_value, step):
        """ It set the component type of the vector variable to real by receiving the minimum and
        maximum values that it will be able to have, and the step size to traverse the interval

        :param vector_variable_name: Vector variable name previously defined.
        :param min_value: Minimum value.
        :param max_value: Maximum value.
        :param step: Step size.
        :type vector_variable_name: str
        :type min_value: float
        :type max_value: float
        :type step: float
        """
        self.__definitions[vector_variable_name][4] = [REAL, min_value, max_value, step]

    def set_vector_component_to_categorical(self, vector_variable_name, categories):
        """ It set the component type of the vector variable to categorical by receiving a list with
        the labels that it will be able to have.

        :param vector_variable_name: Vector variable name previously defined.
        :param categories: List of label.
        :type vector_variable_name: str
        :type categories: list
        """
        self.__definitions[vector_variable_name][4] = [CATEGORICAL, categories]

    def set_vector_component_to_layer(self, vector_variable_name):
        """ It set the component type of the vector variable to layer. Afterwards, the components of
        the layer must be set using the methods:

        - :py:meth:`~pycvoa.definition.ProblemDefinition.insert_integer_in_vector_layer_component`
        - :py:meth:`~pycvoa.definition.ProblemDefinition.insert_real_in_vector_layer_component`
        - :py:meth:`~pycvoa.definition.ProblemDefinition.insert_categorical_in_vector_layer_component`

        :param vector_variable_name: Vector variable name previously defined.
        :type vector_variable_name: str
        """
        self.__definitions[vector_variable_name][4] = [LAYER, {}]

    def insert_integer_in_vector_layer_component(self, vector_variable_name, element_name, min_value, max_value, step):
        """ It defines an integer element of a vector variable set as a layer by receiving the minimum and
        maximum values that it will be able to have, and the step size to traverse the interval.

        :param vector_variable_name: Vector variable name previously defined.
        :param element_name: Element name.
        :param min_value: Minimum value.
        :param max_value: Maximum value.
        :param step: Step size.
        :type vector_variable_name: str
        :type element_name: str
        :type min_value: int
        :type max_value: int
        :type step: int
        """
        layer_definition = self.__definitions[vector_variable_name][4]
        layer_elements = layer_definition[1]
        layer_elements[element_name] = [INTEGER, min_value, max_value, step]

    def insert_real_in_vector_layer_component(self, vector_variable_name, element_name, min_value, max_value, step):
        """ It defines a real element of a vector variable set as a layer by receiving the minimum and
        maximum values that it will be able to have, and the step size to traverse the interval.

        :param vector_variable_name: Vector variable name previously defined.
        :param element_name: Element name.
        :param min_value: Minimum value.
        :param max_value: Maximum value.
        :param step: Step size.
        :type vector_variable_name: str
        :type element_name: str
        :type min_value: float
        :type max_value: float
        :type step: float
        """
        layer_definition = self.__definitions[vector_variable_name][4]
        layer_elements = layer_definition[1]
        layer_elements[element_name] = [REAL, min_value, max_value, step]

    def insert_categorical_in_vector_layer_component(self, vector_variable_name, element_name, categories):
        """ It defines a categorical element of a vector variable set as a layer by receiving a list with
        the labels that it will be able to have.

        :param vector_variable_name: Vector variable name previously defined.
        :param element_name: Element name.
        :param categories: List of labels.
        :type vector_variable_name: str
        :type element_name: str
        :type categories: list
        """
        layer_definition = self.__definitions[vector_variable_name][4]
        layer_elements = layer_definition[1]
        layer_elements[element_name] = [CATEGORICAL, categories]

    def get_internal_definition(self):
        """ Get the internal data structure for the :py:class:`~pycvoa.individual.ProblemDefinition`

        :returns: Internal structure of the Problem Definition.
        :rtype: dict
        """
        return self.__definitions

    def get_definition_list(self):
        """ Get a list with the registered variables and its definitions in a (key, value) form. It is useful to
        iterate throw the registered variables using a for loop.

        :returns: A (key, value) list with the registered variables.
        :rtype: list
        """
        return self.__definitions.items()

    def get_variable_list(self):
        """ Get a list with the registered variables. It is useful to iterate throw the registered variables
        using a for loop.

        :returns: A list with the registered variables.
        :rtype: list
        """
        return list(self.__definitions.keys())

    def get_variable_definition(self, variable):
        """ Get the definition of a variable.

        :param variable: The variable.
        :type variable: str
        :returns: Definition of a variable.
        :rtype: list
        """
        return self.__definitions[variable]

    def get_variable_type(self, variable):
        """ Get the variable type.

        :param variable: The variable.
        :type variable: str
        :returns: The variable type.
        :rtype: **INTEGER**, **REAL**, **CATEGORICAL**, **LAYER**, **VECTOR**
        """
        return self.__definitions[variable][0]

    def get_layer_element_list(self, layer_variable):
        """ Get a list with the elements of a registered **LAYER** variable. It is useful to iterate throw
        the elements of a registered **LAYER** variable using a for loop.

        :param layer_variable: The registered layer variable.
        :type layer_variable: str
        :returns: A list with the elements the registered **LAYER** variable.
        :rtype: list
        """
        return list(self.__definitions[layer_variable][1].keys())

    def get_layer_element_type(self, layer_variable, element):
        """ Get the layer element type.

        :param layer_variable: The registered layer variable.
        :type layer_variable: str
        :param element: The element.
        :type element: str
        :returns: The variable type.
        :rtype: **INTEGER**, **REAL**, **CATEGORICAL**
        """
        return self.__definitions[layer_variable][1][element][0]

    def get_layer_element_definition(self, layer_variable, element):
        """ Get the layer element definition.

        :param layer_variable: The registered layer variable.
        :type layer_variable: str
        :param element: The element.
        :type element: str
        :returns: The element definition.
        :rtype: list
        """
        return self.__definitions[layer_variable][1][element]

    def get_vector_component_type(self, vector_variable):
        """ Get the type of the components of a registered **VECTOR** variable.

        :param vector_variable: The registered **VECTOR** variable.
        :type vector_variable: str
        :returns: The **VECTOR** variable component type.
        :rtype: **INTEGER**, **REAL**, **CATEGORICAL**, **LAYER**
        """
        return self.__definitions[vector_variable][4][0]

    def get_vector_component_definition(self, vector_variable):
        """ Get the definition of the components of a registered **VECTOR** variable.

        :param vector_variable: The registered **VECTOR** variable.
        :type vector_variable: str
        :returns: The **VECTOR** variable component definition.
        :rtype: list
        """
        return self.__definitions[vector_variable][4]

    def get_vector_layer_element_list(self, vector_variable):
        """ Get a list with the elements of a registered **VECTOR** variable registered as **LAYER**. It is useful to
        iterate throw the elements of the layers in a registered **LAYER** variable using a for loop.

        :param vector_variable: The registered **VECTOR** variable.
        :type vector_variable: str
        :returns: A list with the elements of the **LAYER** defined in the **VECTOR** variable.
        :rtype: list
        """
        return list(self.__definitions[vector_variable][4][1].keys())

    def get_vector_layer_element_definition(self, vector_variable, element):
        """ Get the layer element definition for a **VECTOR** variable.

        :param vector_variable: The registered **VECTOR** variable.
        :type vector_variable: str
        :param element: The element.
        :type element: str
        :returns: The element definition.
        :rtype: list
        """
        return self.__definitions[vector_variable][4][1][element]

    def __str__(self):
        """ String representation of a :py:class:`~pycvoa.definition.ProblemDefinition` object
        """
        res = ""
        count = 1
        for k, v in self.__definitions.items():
            res += variable_definition_to_string(k, v)
            if count != len(self.__definitions.items()):
                res += "\n"
            count += 1

        return res
