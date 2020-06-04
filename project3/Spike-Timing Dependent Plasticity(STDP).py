import numpy as np
from matplotlib.pyplot import *
import random
import math

random.seed(10)


def get_fire_pattern(simulation_time=1000):
    fire_pattern = [0] * simulation_time
    cool_down = 0
    for i in range(simulation_time):
        if cool_down == 0 and random.random() > 0.5:
            fire_pattern[i] = 1
            cool_down = math.floor(10 + random.random() * (20 + random.random() * 5))
        else:
            if cool_down > 0:
                cool_down -= 1
    return fire_pattern


def zigma_delta(fire_pattern, time):
    result = 0
    for i in range(10):
        result += 2 ** -i * fire_pattern[time - i]
    return result


def A_plus(w):
    if w > 1:
        return 0
    return 1


def A_minus(w):
    if w == 0:
        return 0
    return 1


time = 30
steps = 0.125

timer = np.arange(0, time + steps, steps)
x = [0] * len(timer)
x_fire_pattern = get_fire_pattern(len(timer))
y = [0] * len(timer)
y_fire_pattern = get_fire_pattern(len(timer))

tau_plus = 10
tau_minus = 10

# a_minus = 0.1
# a_plus = -a_minus*tau_minus / tau_plus * 1.05
a_minus = 0.1
a_plus = 0.1

w = [0] * len(timer)
delta_w = [0] * len(timer)

w[-1] = 1
for i in range(len(timer)):
    # # X
    x[i] = x[i - 1] + ((-x[i - 1]) / tau_plus + x_fire_pattern[i])
    if x[i] < 0:
        x[i] = 0

    # # Y
    y[i] = y[i - 1] + ((-y[i - 1]) / tau_minus + y_fire_pattern[i])
    if y[i] < 0:
        y[i] = 0

    # # W
    delta_w[i] = (-a_minus * A_minus(w[i - 1]) * y[i - 1] * x_fire_pattern[i - 1]) + (a_plus * A_plus(w[i - 1]) * x[i - 1] * y_fire_pattern[i - 1])
    w[i] = w[i - 1] + delta_w[i]

# # ploting
fig = figure(num=None, figsize=(20, 20))
subplot(311)
plot(timer, x)
ylabel('X_i')
xlabel('Time')
title('X_i - Time plot')
grid(True)
subplot(312)
plot(timer, y)
ylabel('Y_i')
xlabel('Time')
title('Y_i - Time plot')
grid(True)
subplot(313)
plot(timer, w)
ylabel('W')
xlabel('Time')
title('W - Time plot')
grid(True)
savefig('../figures/project3/STDP X_i Y_i W.png')
show()

x_axis = []
y_axis = []
for i in range(len(timer)):
    if delta_w[i] != 0:
        x_axis.append(timer[i-2])
        y_axis.append(delta_w[i]/w[i] )
fig = figure(num=None, figsize=(20, 20))
scatter(x_axis, y_axis, s=20)
plot(x_axis, y_axis)
for i in range(len(timer)):
    if y_fire_pattern[i] == 1:
        axvline(timer[i], color='r', alpha=0.7)
# for i in range(len(timer)):
#     if x_fire_pattern[i] == 1:
#         axvline(timer[i], color='g', alpha=0.7)
axhline(0, color='r')
ylabel('delta_w')
xlabel('Time')
title('delta_w - Time plot')
# grid(True)
savefig('../figures/project3/STDP delta W.png')
show()
