from dnnv.properties import *

N = Network("N")

Forall(
    x,
    Implies(
        (0 <= x <= 1),
        And(
            abs(N(x)[0, 7] - N(x)[0, 2]) < abs(N(x)[0, 7] - N(x)[0, 5]),
            abs(N(x)[0, 7] - N(x)[0, 2]) < abs(N(x)[0, 2] - N(x)[0, 5]),
        ),
    ),
)
