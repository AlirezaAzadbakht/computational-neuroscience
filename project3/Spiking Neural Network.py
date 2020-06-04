from project3.Neuron import Neuron
from project3.Neuron import Random_input
import matplotlib.patches as mpatches
from matplotlib.pyplot import *
import random
import math

random.seed(1)


def A_plus(w):
    if w > 1:
        return 0
    return 1


def A_minus(w):
    if w == 0:
        return 0
    return 1


def get_input_spikes(i, freq_pattern1=10, freq_pattern2=5):
    if i % freq_pattern1 == 0:
        state = 4
    elif i % freq_pattern1 == 1:
        state = 3
    elif i % freq_pattern2 == 0:
        state = 2
    elif i % freq_pattern2 == 1:
        state = 1
    else:
        state = 0

    if i in [2300, 2302, 2304]:
        state = 4
    elif i in [2301, 2303, 2305]:
        state = 3
    elif i in [2400, 2402, 2404]:
        state = 2
    elif i in [2401, 2403, 2405]:
        state = 1
    elif i in [2500, 2501, 2502 , 2503,2504]:
        state = 0
    elif i > 2000:
        return [0] * n

    if state == 4:
        # pattern 2
        return [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    elif state == 3:
        # pattern 2
        return [0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
    elif state == 2:
        # pattern 1
        return [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
    elif state == 1:
        # pattern 1
        return [0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
    elif state == 0:
        # Random firing
        a = [0] * n
        fire = math.floor(random.random() * n)
        a[fire] = 1
        return a


def spike_response_function(s, time_constant_controlling=2):
    h = 1
    if s <= 0:
        h = 0
    result = (s / time_constant_controlling) * math.exp(1 - s / time_constant_controlling) * h
    if result < 0.01:
        return 0
    return (s / time_constant_controlling) * math.exp(1 - s / time_constant_controlling) * h


n = 10

output1 = Neuron()
output2 = Neuron()

w1 = []
d1 = []
w2 = []
d2 = []
for i in range(n):
    # w1.append(random.random())
    w1.append(1)
    d1.append(random.random())
    # w2.append(random.random())
    w2.append(1)
    d2.append(random.random())

update_queue = []
for i in range(n):
    update_queue.append([])

simulation_length = len(output1.timer)

# STDP params
x1 = []
x2 = []
y1 = []
y2 = []
for i in range(n):
    x1.append([0] * simulation_length)
    x2.append([0] * simulation_length)
    y1.append([0] * simulation_length)
    y2.append([0] * simulation_length)

# gmax = 1

tau_plus = 2
tau_minus = 2

# a_minus = 0.1
# a_plus = -a_minus * tau_minus / tau_plus * 1.05
a_minus = 0.01
a_plus = 0.01

# a_minus *= gmax
# a_plus *= gmax

delta_w1 = [0] * simulation_length
delta_w2 = [0] * simulation_length

plot(w1 , color = 'g')
plot(w2, color = 'r')
ylabel('Weight')
xlabel('Input Connection Index')
title('Input Weights of Two Outputs Neurons - step:0')
green_patch = mpatches.Patch(color='green', label='Input Weights of Neuron 1')
red_patch = mpatches.Patch(color='red', label='Input Weights of Neuron 2')
legend(handles=[green_patch, red_patch])
savefig('../figures/project3/Input Weights Animation (fixed init)-step0.png')
show()

for current_time in range(simulation_length):
    if current_time % 200 == 0 and current_time<=2000:
        plot(w1 , color = 'g')
        plot(w2, color = 'r')
        ylabel('Weight')
        xlabel('Input Connection Index')
        title('Input Weights of Two Outputs Neurons - step:'+str(current_time//200+1))
        green_patch = mpatches.Patch(color='green', label='Input Weights of Neuron 1')
        red_patch = mpatches.Patch(color='red', label='Input Weights of Neuron 2')
        legend(handles=[green_patch, red_patch])
        savefig('../figures/project3/Input Weights Animation (fixed init)-step'+str(current_time//200+1)+'.png')
        show()
    print(int(current_time / simulation_length * 10000) / 100, "%")
    fire_pattern = get_input_spikes(current_time)
    for i in range(n):
        if fire_pattern[i] == 1:
            update_queue[i].append(current_time)

    # output neuron 1
    input_temp = 0
    for i in range(n):
        for past_fire_time in update_queue[i]:
            input_temp += w1[i] * spike_response_function(current_time - past_fire_time - d1[i])
            # if i ==9:
            #     print(spike_response_function(current_time - past_fire_time - d1[i]))
    fired = output1.update(j=current_time, input=input_temp)
    # print(input_temp)
    for i in range(n):
        ## X
        x1[i][current_time] = x1[i][current_time - 1] + ((-x1[i][current_time - 1]) / tau_plus + fire_pattern[i])
        if x1[i][current_time] < 0:
            x1[i][current_time] = 0
        ## Y
        y_fire_pattern = 0
        if fired > 0:
            y_fire_pattern = 1
        y1[i][current_time] = y1[i][current_time - 1] + ((-y1[i][current_time - 1]) / tau_minus + y_fire_pattern)
        if y1[i][current_time] < 0:
            y1[i][current_time] = 0

        ## W
        delta_w = (-a_minus * A_minus(w1[i - 1]) * y1[i][current_time - 1] * fire_pattern[i]) + (
                    a_plus * A_plus(w1[i - 1]) * x1[i][current_time - 1] * y_fire_pattern)
        w1[i] = w1[i] + delta_w
        if w1[i] < 0:
            w1[i] = 0.01

    # output neuron 2
    input_temp = 0
    for i in range(n):
        for past_fire_time in update_queue[i]:
            input_temp += w2[i] * spike_response_function(current_time - past_fire_time - d2[i])
    fired = output2.update(j=current_time, input=input_temp)
    for i in range(n):
        ## X
        x2[i][current_time] = x2[i][current_time - 1] + ((-x2[i][current_time - 1]) / tau_plus + fire_pattern[i])
        if x2[i][current_time] < 0:
            x2[i][current_time] = 0
        ## Y
        y_fire_pattern = 0
        if fired > 0:
            y_fire_pattern = 1
        y2[i][current_time] = y2[i][current_time - 1] + ((-y2[i][current_time - 1]) / tau_minus + y_fire_pattern)
        if y2[i][current_time] < 0:
            y2[i][current_time] = 0

        ## W
        delta_w = (-a_minus * A_minus(w2[i - 1]) * y2[i][current_time - 1] * fire_pattern[i]) + (
                    a_plus * A_plus(w2[i - 1]) * x2[i][current_time - 1] * y_fire_pattern)
        w2[i] = w2[i] + delta_w
        if w2[i] < 0:
            w2[i] = 0.01

fig = figure(num=None, figsize=(20, 10))
subplot(211)
plot(output1.timer, output1.u)
ylabel('U')
xlabel('Time')
title('Output Neuron 1')
grid(True)

subplot(212)
plot(output2.timer, output2.u)
ylabel('U')
xlabel('Time')
title('Output Neuron 2')
grid(True)
savefig('../figures/project3/Output Neurons (fixed init).png')
show()

print("==")
print(w1)
print(w2)

