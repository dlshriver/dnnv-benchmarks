from dnnv.properties import *
import numpy as np

N1 = Network("N1")
N2 = Network("N2")

class_1 = 6
class_2 = 3

Forall(
    x,
    Implies(
        (0 <= x <= 1),
        (np.argmax(N1(x)) != class_1) | (np.argmax(N2(x)) != class_2),
    ),
)
