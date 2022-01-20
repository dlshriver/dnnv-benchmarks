from dnnv.properties import *

N = Network("N")

Forall(
    x,
    Implies(
        (0 <= x <= 1),
        And(
            abs(N(x)[0, 8] - N(x)[0, 5]) < abs(N(x)[0, 8] - N(x)[0, 4]),
            abs(N(x)[0, 8] - N(x)[0, 5]) < abs(N(x)[0, 5] - N(x)[0, 4]),
        ),
    ),
)
