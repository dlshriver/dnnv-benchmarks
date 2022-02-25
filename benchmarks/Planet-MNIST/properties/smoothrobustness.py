from dnnv.properties import *
from pathlib import Path
import numpy as np

N = Network("N")
input_path = Parameter(
    "input_path", Path, default=(__path__.parent / "inputs/imageOf3.npy")
)
x0 = np.load(input_path)[None]
gamma = Parameter("gamma", float, default=0.05)
prohibited_class = Parameter("prohibited_class", int, default=4)

Forall(
    x,
    Implies(
        And(
            # must be input domain
            0 <= x <= 1,
            # require pixels within 3 pixels of a border to remain the same
            # height
            x0[:, :, :3, :] <= x[:, :, :3, :],
            x[:, :, :3, :] <= x0[:, :, :3, :],
            x0[:, :, -3:, :] <= x[:, :, -3:, :],
            x[:, :, -3:, :] <= x0[:, :, -3:, :],
            # width
            x0[:, :, :, :3] <= x[:, :, :, :3],
            x[:, :, :, :3] <= x0[:, :, :, :3],
            x0[:, :, :, -3:] <= x[:, :, :, -3:],
            x[:, :, :, -3:] <= x0[:, :, :, -3:],
            # constrain the smoothness of the perturbation
            x0[:, :, :-1, :] - x0[:, :, 1:, :] - gamma
            <= x[:, :, :-1, :] - x[:, :, 1:, :],
            x0[:, :, :-1, :] - x0[:, :, 1:, :] + gamma
            >= x[:, :, :-1, :] - x[:, :, 1:, :],
            x0[:, :, :, :-1] - x0[:, :, :, 1:] - gamma
            <= x[:, :, :, :-1] - x[:, :, :, 1:],
            x0[:, :, :, :-1] - x0[:, :, :, 1:] + gamma
            >= x[:, :, :, :-1] - x[:, :, :, 1:],
        ),
        np.argmax(N(x)) != prohibited_class,
    ),
)
