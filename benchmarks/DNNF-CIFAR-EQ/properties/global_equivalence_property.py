from dnnv.properties import *
import numpy as np

N1 = Network("N1")
N2 = Network("N2")

Forall(
    x,
    Implies(
        (0 <= x <= 1),
        (np.argmax(N1(x)) == np.argmax(N2(x))),
    ),
)
