from dnnv.properties import *
import numpy as np

N = Network("N")
N_prob_coll = N[2:-3, 1]  # get pre-sigmoid value
N_steer_angle = N[2:-1, 0]

logit = lambda x: np.log(x / (1 - x))
P_coll_min = logit(0.7)
P_coll_max = logit(0.8)

steer_max = 70 * np.pi / 180

Forall(
    x,
    Implies(
        And(0 <= x <= 1, P_coll_min < N_prob_coll(x) <= P_coll_max),
        -steer_max <= N_steer_angle(x) <= steer_max,
    ),
)
