from dnnv.properties import *
import numpy as np

N1 = Network("N1")
N2 = Network("N2")

x = Image("properties/input_4.npy")

epsilon = Parameter("epsilon", type=float)
true_class = 3
other_class = 6

Forall(
    x_,
    Implies(
        ((x - epsilon) < x_ < (x + epsilon)) & (0 <= x_ <= 1),
        And(
            Implies(np.argmax(N1(x_)) == true_class, np.argmax(N2(x_)) != other_class),
            Implies(np.argmax(N2(x_)) == true_class, np.argmax(N1(x_)) != other_class),
        )
    ),
)
