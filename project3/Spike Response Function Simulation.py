import math
from matplotlib.pyplot import *


def spike_response_function(s, time_constant_controlling=10):
    h = 1
    if s <= 0:
        h = 0
    result = (s / time_constant_controlling) * math.exp(1 - s / time_constant_controlling) * h
    if result < 0.01:
        return 0
    return (s / time_constant_controlling) * math.exp(1 - s / time_constant_controlling) * h


u = [0] * 100
for i in range(100):
    u[i] = spike_response_function(i - 20 - 5)

plot(range(100), u)
axvline(20, color='r')
savefig('../figures/project3/spike response function.png')
show()
