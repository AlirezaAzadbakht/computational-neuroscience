from project3.Neuron import Neuron
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
    elif i in [2500, 2501, 2502, 2503, 2504]:
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
inhibitory = Neuron(type='inh')

w1 = []
d1 = []
w2 = []
d2 = []
w3 = []
d3 = []

wh1 = 1
dh1 = 0
wh2 = 1
dh2 = 0
for i in range(n):
    w1.append(random.random())
    # w1.append(1)
    # d1.append(random.random())
    d1.append(1)

    w2.append(random.random())
    # w2.append(1)
    # d2.append(random.random())
    d2.append(1)

    w3.append(random.random())
    # w3.append(1)
    d3.append(0)

update_queue = []
update_queue_h = []
for i in range(n):
    update_queue.append([])

simulation_length = len(output1.timer)

# STDP params
x1 = []
x2 = []
x3 = []
y1 = []
y2 = []
y3 = []

xh1 = [0] * simulation_length
xh2 = [0] * simulation_length
yh1 = [0] * simulation_length
yh2 = [0] * simulation_length
for i in range(n):
    x1.append([0] * simulation_length)
    x2.append([0] * simulation_length)
    x3.append([0] * simulation_length)
    y1.append([0] * simulation_length)
    y2.append([0] * simulation_length)
    y3.append([0] * simulation_length)

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
delta_w3 = [0] * simulation_length

plot(w1, color='g')
plot(w2, color='r')
plot(w3, color='b')
ylabel('Weight')
xlabel('Input Connection Index')
title('Input Weights of Two Outputs Neurons and One Inhibitory Neuron - step:0')
green_patch = mpatches.Patch(color='green', label='Input Weights of Neuron 1')
red_patch = mpatches.Patch(color='red', label='Input Weights of Neuron 2')
blue_patch = mpatches.Patch(color='blue', label='Input Weights of Inhibitory Neuron')
legend(handles=[green_patch, red_patch, blue_patch])
savefig('../figures/project3/Input Weights Animation with inhibitory test-step0.png')
show()

for current_time in range(simulation_length):
    if current_time % 200 == 0 and current_time <= 2000:
        plot(w1, color='g')
        plot(w2, color='r')
        plot(w3, color='b')
        ylabel('Weight')
        xlabel('Input Connection Index')
        title('Input Weights of Two Outputs Neurons and One Inhibitory Neuron - step:' + str(current_time // 200 + 1))
        green_patch = mpatches.Patch(color='green', label='Input Weights of Neuron 1')
        blue_patch = mpatches.Patch(color='blue', label='Input Weights of Inhibitory Neuron')
        legend(handles=[green_patch, red_patch, blue_patch])
        savefig('../figures/project3/Input Weights Animation with inhibitory test-step' + str(current_time // 200 + 1) + '.png')
        show()
    print(int(current_time / simulation_length * 10000) / 100, "%")
    fire_pattern = get_input_spikes(current_time)
    for i in range(n):
        if fire_pattern[i] == 1:
            update_queue[i].append(current_time)

    # output neuron 1
    output1_fired = 0
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
            output1_fired = 1
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
    output2_fired = 0
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
            output2_fired = 1
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

    # inhibitory neuron
    input_temp = 0
    for i in range(n):
        for past_fire_time in update_queue[i]:
            input_temp += w3[i] * spike_response_function(current_time - past_fire_time - d3[i])
    fired = inhibitory.update(j=current_time, input=input_temp)
    ##################################################################################################################################
    # lets inhibits others
    y_fire_pattern = 0
    if fired > 0:
        y_fire_pattern = 1
        update_queue_h.append(current_time)
    if fired > 0:
        print(fired)
        for past_fire_time in update_queue_h:
            output1.update(j=current_time + 1, input=-wh1 * spike_response_function(current_time - past_fire_time - dh1))
            output2.update(j=current_time + 1, input=-wh2 * spike_response_function(current_time - past_fire_time - dh2))
    # n 1
    # # X
    xh1[i] = xh1[i - 1] + ((-xh1[i - 1]) / tau_plus + output1_fired)
    if xh1[i] < 0:
        xh1[i] = 0

    # # Y
    yh1[i] = yh1[i - 1] + ((-yh1[i - 1]) / tau_minus + y_fire_pattern)
    if yh1[i] < 0:
        yh1[i] = 0

    # # W
    delta_w = (-a_minus * A_minus(wh1) * yh1[i - 1] * output1_fired) + (
            a_plus * A_plus(wh1) * xh1[i - 1] * y_fire_pattern)
    wh1 = wh1 + delta_w

    # n2
    # # X
    xh2[i] = xh2[i - 1] + ((-xh2[i - 1]) / tau_plus + output2_fired)
    if xh2[i] < 0:
        xh2[i] = 0

    # # Y
    yh2[i] = yh2[i - 1] + ((-yh2[i - 1]) / tau_minus + y_fire_pattern)
    if yh2[i] < 0:
        yh2[i] = 0

    # # W
    delta_w = (-a_minus * A_minus(wh1) * yh2[i - 1] * output2_fired) + (
            a_plus * A_plus(wh1) * xh2[i - 1] * y_fire_pattern)
    wh2 = wh2 + delta_w

    ##################################################################################################################################
    for i in range(n):
        ## X
        x3[i][current_time] = x3[i][current_time - 1] + ((-x3[i][current_time - 1]) / tau_plus + fire_pattern[i])
        if x3[i][current_time] < 0:
            x3[i][current_time] = 0
        ## Y
        y_fire_pattern = 0
        if fired > 0:
            y_fire_pattern = 1
        y3[i][current_time] = y3[i][current_time - 1] + ((-y3[i][current_time - 1]) / tau_minus + y_fire_pattern)
        if y3[i][current_time] < 0:
            y3[i][current_time] = 0

        ## W
        delta_w = (-a_minus * A_minus(w3[i - 1]) * y3[i][current_time - 1] * fire_pattern[i]) + (
                a_plus * A_plus(w3[i - 1]) * x3[i][current_time - 1] * y_fire_pattern)
        w3[i] = w3[i] + delta_w
        if w3[i] < 0:
            w3[i] = 0.01

fig = figure(num=None, figsize=(20, 10))
subplot(311)
plot(output1.timer, output1.u)
ylabel('U')
title('Output Neuron 1')
grid(True)

subplot(312)
plot(output2.timer, output2.u)
ylabel('U')
title('Output Neuron 2')
grid(True)

subplot(313)
plot(inhibitory.timer, inhibitory.u)
ylabel('U')
xlabel('Time')
title('Inhibitory Neuron')
grid(True)
savefig('../figures/project3/Output Neurons with inhibitory test.png')
show()

print("==")
print(w1)
print(w2)
print(w3)
print(wh1)
print(wh2)
