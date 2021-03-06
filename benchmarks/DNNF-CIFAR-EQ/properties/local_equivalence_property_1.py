from dnnv.properties import *
import numpy as np

N1 = Network("N1")
N2 = Network("N2")

x = Image(__path__.parent / "input_1.npy")

epsilon = Parameter("epsilon", type=float)

Forall(
    x_,
    Implies(
        ((x - epsilon) < x_ < (x + epsilon)) & (0 <= x_ <= 1),
        np.argmax(N1(x_)) == np.argmax(N2(x_)),
    ),
)
