from dnnv.properties import *
from pathlib import Path
import numpy as np

N = Network("N")
input_path = Parameter(
    "input_path", Path, default=(__path__.parent / "inputs/imageOf3.npy")
)
x0 = np.load(input_path)[None]
epsilon = Parameter("epsilon", float)  # original properties used 0.08 and 0.12
prohibited_class = Parameter("prohibited_class", int, default=4)

Forall(
    x,
    Implies(
        And(
            # must be input domain
            0 <= x <= 1,
            # center of image is allowed to change by epsilon
            # any pixel at least 3 pixels from a border can change
            x0[:, :, 3:-3, 3:-3] - epsilon <= x[:, :, 3:-3, 3:-3],
            x[:, :, 3:-3, 3:-3] <= x0[:, :, 3:-3, 3:-3] + epsilon,
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
        ),
        np.argmax(N(x)) != prohibited_class,
    ),
)
