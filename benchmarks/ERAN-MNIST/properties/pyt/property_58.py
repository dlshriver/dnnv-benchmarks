from dnnv.properties import *
import numpy as np

N = Network("N")
mean = 0.1307
stddev = 0.3081
denormalize = lambda x: x * stddev + mean
# x is not normalized
x = Image(__path__.parent.parent / "inputs/input58.npy")

epsilon = Parameter("epsilon", type=float, default=(2.0 / 255))
true_class = 9

Forall(
    x_,  # x_ is assumed to be normalized, so denormalize before comparing to x
    Implies(
        ((x - epsilon) < denormalize(x_) < (x + epsilon)) & (0 < denormalize(x_) < 1),
        np.argmax(N(x_)) == true_class,
    ),
)
