from pycvoa.problem.domain import Domain

example_domain: Domain = Domain()
example_domain.define_integer("I", 0, 100)
example_domain.define_real("R", 0.0, 1.0)
example_domain.define_categorical("C", ["C1", "C2", "C3", "C4"])
example_domain.define_layer("L")
example_domain.define_integer_element("L", "EI", 0, 100)
example_domain.define_real_element("L", "ER", 1.5, 3.0)
example_domain.define_categorical_element("L", "EC", ["Lb1", "Lb2", "Lb3"])
example_domain.define_vector("VN", 2, 8)
example_domain.define_vector("VI", 10, 30)
example_domain.define_components_as_integer("VI", 1, 10)
example_domain.define_vector("VR", 1, 10)
example_domain.define_components_as_real("VR", 0.0, 0.1)
example_domain.define_vector("VC", 10, 15)
example_domain.define_components_as_categorical("VC", ["V1", "V2", "V3"])
example_domain.define_vector("VL", 2, 4)
example_domain.define_components_as_layer("VL")
example_domain.define_layer_vector_integer_element("VL", "el1", 10, 20)
example_domain.define_layer_vector_real_element("VL", "el2", 0.1, 0.5)
example_domain.define_layer_vector_categorical_element("VL", "el3", [1, 2, 3])
