from dnnv.properties import *
import numpy as np

N1 = Network("N1")
N2 = Network("N2")

class_1 = 1
class_2 = 8

Forall(
    x,
    Implies(
        (0 <= x <= 1),
        (np.argmax(N1(x)) != class_1) | (np.argmax(N2(x)) != class_2),
    ),
)
