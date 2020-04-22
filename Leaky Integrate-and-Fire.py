import numpy as np
from matplotlib.pyplot import *
import random
import math


def i_interval(x, i):
    if 20 < x < 70:
        return i
    return 0


def i_random(x, i):
    return random.random() * i


def lif(time=100, steps=0.125, i_function=i_interval, u_rest=0, r=1, c=10, i=5, threshold=2, f_i_plot=False,
        save_name="LIF"):
    timer = np.arange(0, time + steps, steps)
    tm = r * c
    u = [u_rest] * len(timer)
    dt = steps
    i_input = [i_function(j, i) for j in timer]

    # LIF Model -> NEURONAL DYNAMICS [Wulfram_Gerstner,_Werner_M_Kistle] page 11
    for j in range(len(timer)):
        u[j] = u[j - 1] + (-u[j - 1] + r * i_input[j]) / tm * dt
        if u[j] >= threshold or u[j] < u_rest:
            u[j] = u_rest

    # plotting
    fig = figure(num=None, figsize=(20, 10))
    fig.suptitle('Leaky Integrate-and-Fire\n\n' + "R: " + str(r) + "    C: " + str(c) + "    I: " + str(
        i) + "    THRESHOLD: " + str(threshold), fontsize=14, fontweight='bold')
    subplot(221)
    plot(timer, u)
    ylabel('U')
    xlabel('Time')
    title('U-Time plot')
    grid(True)

    subplot(222)
    plot(timer, i_input)
    ylabel('I')
    xlabel('Time')
    title('I-Time plot')
    grid(True)

    if f_i_plot:
        i_x = np.arange(0, 5, 0.125)
        i_y = [0] * len(i_x)
        for j in range(len(i_x)):
            try:
                i_y[j] = 1 / (-1 * tm * (math.log(1 - (threshold - u_rest) / (r * j))))
            except:
                i_y[j] = 0
        subplot(223)
        plot(i_x, i_y)
        ylabel('F')
        xlabel('I')
        title('F-I plot')
        grid(True)
    savefig('figures/{}.png'.format(save_name))
    show()


lif(u_rest=0, r=1, c=10, i=5, threshold=2, f_i_plot=True, save_name="LIF1")
lif(u_rest=2, r=10, c=5, i=2, threshold=5, f_i_plot=True, save_name="LIF2")
lif(u_rest=2, r=5, c=7, i=1, threshold=5, f_i_plot=True, save_name="LIF3")
lif(u_rest=0, r=3, c=3, i=10, threshold=2, f_i_plot=True, save_name="LIF4")
lif(u_rest=1, r=2, c=4, i=7, threshold=50, f_i_plot=True, save_name="LIF5")

lif(u_rest=0, r=1, c=10, i=5, threshold=2, i_function=i_random, save_name="LIF_random1")
lif(u_rest=2, r=10, c=5, i=2, threshold=5, i_function=i_random, save_name="LIF_random2")
lif(u_rest=2, r=5, c=7, i=1, threshold=5, i_function=i_random, save_name="LIF_random3")
lif(u_rest=0, r=3, c=3, i=10, threshold=2, i_function=i_random, save_name="LIF_random4")
lif(u_rest=1, r=2, c=4, i=7, threshold=50, i_function=i_random, save_name="LIF_random5")
