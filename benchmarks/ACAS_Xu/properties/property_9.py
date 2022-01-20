"""
Property $\phi_9$.
  - Description: Even if the previous advisory was ``weak right'', the presence of a nearby intruder will cause the network to output a ``strong left'' advisory instead.
  - Tested on: $N_{3,3}$.
  - Input constraints: $2000 \le \rho \le 7000$, $−0.4 \le \theta \le −0.14$, $−3.141592 \le \psi \le −3.141592 + 0.01$, $100 \le v_{own} \le 150$, $0 \le v_{int} \le 150$.
  - Desired output property: the score for ``strong left'' is minimal.
"""
from dnnv.properties import *
import numpy as np

N = Network("N")
# x: $\rho$, $\theta$, $\psi$, $v_{own}$, $v_{int}$
# x_{min}: 0.0, -3.141593, -3.141593, 100.0, 0.0
# x_{max}: 60760.0, 3.141593, 3.141593, 1200.0, 1200.0
x_min = np.array([[2000.0, -0.4, -3.141592, 100.0, 0.0]])
x_max = np.array([[7000.0, -0.14, -3.141592 + 0.01, 150.0, 150.0]])

x_mean = np.array([[1.9791091e04, 0.0, 0.0, 650.0, 600.0]])
x_range = np.array([[60261.0, 6.28318530718, 6.28318530718, 1100.0, 1200.0]])

x_min_normalized = (x_min - x_mean) / x_range
x_max_normalized = (x_max - x_mean) / x_range

# y: Clear-of-Conflict, weak left, weak right, strong left, strong right
y_mean = 7.5188840201005975
y_range = 373.94992

Forall(
    x,
    Implies(x_min_normalized <= x <= x_max_normalized, np.argmin(N(x)) == 3),
)
