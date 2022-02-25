from dnnv.properties import *

N = Network("N")
digit = Parameter("digit", int, default=2)
delta = Parameter("delta", float)

Forall(
    x,
    Implies(
        0 <= x <= 1,
        Or(
            (N(x)[0][digit] < N(x)[0, 0] + delta) if digit != 0 else False,
            (N(x)[0][digit] < N(x)[0, 1] + delta) if digit != 1 else False,
            (N(x)[0][digit] < N(x)[0, 2] + delta) if digit != 2 else False,
            (N(x)[0][digit] < N(x)[0, 3] + delta) if digit != 3 else False,
            (N(x)[0][digit] < N(x)[0, 4] + delta) if digit != 4 else False,
            (N(x)[0][digit] < N(x)[0, 5] + delta) if digit != 5 else False,
            (N(x)[0][digit] < N(x)[0, 6] + delta) if digit != 6 else False,
            (N(x)[0][digit] < N(x)[0, 7] + delta) if digit != 7 else False,
            (N(x)[0][digit] < N(x)[0, 8] + delta) if digit != 8 else False,
            (N(x)[0][digit] < N(x)[0, 9] + delta) if digit != 9 else False,
        ),
    ),
)
