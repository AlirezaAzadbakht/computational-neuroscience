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


def explif(time=100, steps=0.125, i_function=i_interval, u_rest=0, r=1, c=10, i=5, threshold=2, delta_t=2, theta_rh=2,
           f_i_plot=False,
           save_name="none",
           draw_plot=True):
    timer = np.arange(0, time + steps, steps)
    tm = r * c
    u = [u_rest] * len(timer)
    dt = steps
    i_input = [i_function(j, i) for j in timer]

    spike_t = time
    current_spike_time = 0

    # ELIF Model -> NEURONAL DYNAMICS [Wulfram_Gerstner,_Werner_M_Kistle] page 124
    for j in range(len(timer)):
        u[j] = u[j - 1] + (-u[j - 1] + r * i_input[j] + delta_t * math.exp((u[j - 1] - theta_rh) / delta_t)) / tm * dt
        if u[j] >= threshold or u[j] < u_rest:
            u[j] = u_rest
            prev_spike_time = current_spike_time
            current_spike_time = timer[j]
            spike_t = min(spike_t, current_spike_time - prev_spike_time)

    # plotting
    if draw_plot:
        fig = figure(num=None, figsize=(20, 10))
        fig.suptitle('Exponential Integrate-and-Fire\n\n' + "R: " + str(r) + "    C: " + str(c) + "    I: " + str(i)
                     + "    THRESHOLD: " + str(threshold) + "    DELTA T: " + str(delta_t)
                     + "    THETA RH: " + str(theta_rh),
                     fontsize=14, fontweight='bold')
        subplot(221)
        plot(timer, u)
        ylabel('U')
        xlabel('Time')
        title('U-Time plot')
        grid(True)

        subplot(223)
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
                    i_y[j] = 1/ explif(time=time, steps=steps, i_function=i_function, u_rest=u_rest, r=r, c=c,
                                        i=i_x[j],
                                        threshold=threshold, delta_t=delta_t, theta_rh=theta_rh, f_i_plot=False,
                                        save_name="none",
                                        draw_plot=False)
                except:
                    i_y[j] = 0
            subplot(222)
            plot(i_x, i_y)
            ylabel('F')
            xlabel('I')
            title('F-I plot')
            grid(True)
        if save_name != 'none':
            savefig('figures/{}.png'.format(save_name))
        show()

    return spike_t


explif(u_rest=2, r=1, c=10, i=5, threshold=7, delta_t=2, theta_rh=2, f_i_plot=True, save_name="ELIF1")
explif(u_rest=2, r=10, c=5, i=2, threshold=5, delta_t=4, theta_rh=3, f_i_plot=True, save_name="ELIF2")
explif(u_rest=2, r=5, c=7, i=1, threshold=5, delta_t=7, theta_rh=3, f_i_plot=True, save_name="ELIF3")
explif(u_rest=0, r=3, c=3, i=4, threshold=2, delta_t=4, theta_rh=1, f_i_plot=True, save_name="ELIF4")
explif(u_rest=1, r=2, c=4, i=2, threshold=5, delta_t=3, theta_rh=3, f_i_plot=True, save_name="ELIF5")
explif(u_rest=1, r=2, c=4, i=7, threshold=40, delta_t=5, theta_rh=10, f_i_plot=False, save_name="ELIF6")

explif(u_rest=2, r=1, c=10, i=5, threshold=7, delta_t=2, theta_rh=2, i_function=i_random, save_name="ELIF_random1")
explif(u_rest=2, r=10, c=5, i=2, threshold=5, delta_t=4, theta_rh=3, i_function=i_random, save_name="ELIF_random2")
explif(u_rest=2, r=5, c=7, i=1, threshold=5, delta_t=7, theta_rh=3,i_function=i_random, save_name="ELIF_random3")
explif(u_rest=0, r=3, c=3, i=4, threshold=2, delta_t=4, theta_rh=1, i_function=i_random, save_name="ELIF_random4")
explif(u_rest=1, r=2, c=4, i=10, threshold=50, delta_t=3, theta_rh=10,i_function=i_random, save_name="ELIF_random5")
