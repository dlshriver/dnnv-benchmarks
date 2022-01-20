from dnnv.properties import *

N = Network("N")

Forall(
    x,
    Implies(
        (0 <= x <= 1),
        And(
            abs(N(x)[0, 6] - N(x)[0, 0]) < abs(N(x)[0, 6] - N(x)[0, 7]),
            abs(N(x)[0, 6] - N(x)[0, 0]) < abs(N(x)[0, 0] - N(x)[0, 7]),
        ),
    ),
)
