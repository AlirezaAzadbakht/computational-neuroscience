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


def AdEx(time=100, steps=0.125, i_function=i_interval, u_rest=0, r=1, c=10, i=5, threshold=3, delta_t=2, theta_rh=2, a=2, b=2, tw=5,
         f_i_plot=False,
         save_name="none",
         draw_plot=True):
    timer = np.arange(0, time + steps, steps)
    tm = r * c
    u = [u_rest] * len(timer)
    w = [0] * len(timer)
    dt = steps
    i_input = [i_function(j, i) for j in timer]
    zigma_delta_funciton = 0

    spike_t = time
    current_spike_time = 0

    # AdEx LIF Model -> NEURONAL DYNAMICS [Wulfram_Gerstner,_Werner_M_Kistle] page 137
    for j in range(len(timer)):
        u[j] = u[j - 1] + (-u[j - 1] + r * i_input[j] + delta_t * math.exp((u[j - 1] - theta_rh) / delta_t) - r * w[j - 1]) / tm * dt
        w[j] = w[j - 1] + (a * u[j - 1] - w[j - 1] + b * tw * zigma_delta_funciton) / tw * dt
        if u[j] >= threshold or u[j] < u_rest:
            u[j] = u_rest
            zigma_delta_funciton += 1
            prev_spike_time = current_spike_time
            current_spike_time = timer[j]
            spike_t = min(spike_t, current_spike_time - prev_spike_time)

    # plotting
    if draw_plot:
        fig = figure(num=None, figsize=(20, 10))
        fig.suptitle('Adaptive Exponential Integrate-and-Fire\n\n' + "R: " + str(r) + "    C: " + str(c) + "    I: " + str(i)
                     + "    THRESHOLD: " + str(threshold) + "    DELTA T: " + str(delta_t)
                     + "    THETA RH: " + str(theta_rh) + "    a: " + str(a) + "    b: " + str(b) + "    Tw: " + str(tw),
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
                    i_y[j] = 1 / AdEx(time=time, steps=steps, i_function=i_function, u_rest=u_rest, r=r, c=c, i=i_x[j], a=a, b=b, tw=tw,
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
            savefig('../figures/{}.png'.format(save_name))
        show()

    return spike_t


AdEx(a=1 , b=1 , tw=4, f_i_plot=True)
AdEx(a=10 , b=1 , tw=4, f_i_plot=True)
# AdEx(a=1 , b=1 , tw=4, f_i_plot=True, save_name="AdEx1")
# AdEx(a=1 , b=4 , tw=4, f_i_plot=True, save_name="AdEx2")
# AdEx(a=5 , b=4 , tw=4, f_i_plot=True, save_name="AdEx3")
# AdEx(threshold=5, theta_rh=4, a=1, b=1, tw=4, f_i_plot=True, save_name="AdEx4")
# AdEx(threshold=5, theta_rh=4, i=10, a=1, b=1, tw=1, f_i_plot=True, save_name="AdEx5")
#
# AdEx(a=1 , b=1 , tw=4, i_function=i_random, save_name="AdEx_random1")
# AdEx(a=1 , b=4 , tw=4, i_function=i_random, save_name="AdEx_random2")
# AdEx(a=5 , b=4 , tw=4, i_function=i_random, save_name="AdEx_random3")
# AdEx(threshold=5, theta_rh=4, a=1, b=1, tw=4, i_function=i_random, save_name="AdEx_random4")
# AdEx(threshold=5, theta_rh=4, i=10, a=1, b=1, tw=1, i_function=i_random, save_name="AdEx_random5")