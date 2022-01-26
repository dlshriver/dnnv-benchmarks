from dnnv.properties import *
import numpy as np

N = Network("N")
x = Image(__path__.parent.parent / "inputs/input31.npy")

epsilon = Parameter("epsilon", type=float, default=(2.0 / 255))
true_class = 1

Forall(
    x_,
    Implies(
        ((x - epsilon) < x_ < (x + epsilon)) & (0 < x_ < 1),
        np.argmax(N(x_)) == true_class,
    ),
)
