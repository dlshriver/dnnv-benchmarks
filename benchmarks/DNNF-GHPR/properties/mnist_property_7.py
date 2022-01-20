from dnnv.properties import *

N = Network("N")

Forall(
    x,
    Implies(
        (0 <= x <= 1),
        And(
            abs(N(x)[0, 7] - N(x)[0, 1]) < abs(N(x)[0, 7] - N(x)[0, 6]),
            abs(N(x)[0, 7] - N(x)[0, 1]) < abs(N(x)[0, 1] - N(x)[0, 6]),
        ),
    ),
)
