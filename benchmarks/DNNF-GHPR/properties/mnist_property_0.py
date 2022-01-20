from dnnv.properties import *

N = Network("N")

Forall(
    x,
    Implies(
        (0 <= x <= 1),
        And(
            abs(N(x)[0, 4] - N(x)[0, 9]) < abs(N(x)[0, 4] - N(x)[0, 8]),
            abs(N(x)[0, 4] - N(x)[0, 9]) < abs(N(x)[0, 9] - N(x)[0, 8]),
        ),
    ),
)
