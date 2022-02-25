from dnnv.properties import *
import numpy as np

N = Network("N")
input_lb = np.full(N.input_shape[0], -10, dtype=N.input_details[0].dtype)
input_ub = np.full(N.input_shape[0], 10, dtype=N.input_details[0].dtype)

Forall(x, Implies(input_lb <= x <= input_ub, N(x) > 0))
