from pycvoa.problem.domain import Domain

example_domain: Domain = Domain()
example_domain.define_integer("I", 0, 100)
example_domain.define_real("R", 0.0, 1.0)
example_domain.define_categorical("C", ["C1", "C2", "C3", "C4"])
example_domain.define_layer("L")
example_domain.define_integer_element("L", "E_I", 0, 100)
example_domain.define_real_element("L", "E_R", 1.5, 3.0)
example_domain.define_categorical_element("L", "E_C", ["Lb1", "Lb2", "Lb3"])
example_domain.define_vector("V_N", 2, 8)
example_domain.define_vector("V_I", 20, 100)
example_domain.define_components_as_integer("V_I", 1, 10)
example_domain.define_vector("V_R", 1, 10)
example_domain.define_components_as_real("V_R", 0.0, 0.1)
example_domain.define_vector("V_C", 10, 20)
example_domain.define_components_as_categorical("V_C", ["V1", "V2", "V3"])
example_domain.define_vector("V_L", 10, 20)
example_domain.define_components_as_layer("V_L")
example_domain.define_layer_vector_integer_element("V_L", "el-1", 10, 20)
example_domain.define_layer_vector_real_element("V_L", "el-2", 0.1, 0.5)
example_domain.define_layer_vector_categorical_element("V_L", "el-3", [1, 2, 3])
