from project3.Neuron import Neuron
from project3.Neuron import Random_input
from matplotlib.pyplot import *
import random
import math


def get_input_spikes(i):
    if i % 10 == 0:
        state = 4
    elif i % 10 == 1:
        state = 3
    elif i % 5 == 0:
        state = 2
    elif i % 5 == 1:
        state = 1
    else:
        state = 0

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
    if result <0.01:
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
    w1.append(random.random()*10)
    d1.append(random.random()*10)
    w2.append(random.random()*10)
    d2.append(random.random()*10)

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

tau_plus = 5
tau_minus = 5

a_plus = 0.2
a_minus = 0.4

delta_w1 = [0] * simulation_length
delta_w2 = [0] * simulation_length

for current_time in range(simulation_length):
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
        delta_w = (-a_minus * w1[i] * y1[i][current_time - 1] * fire_pattern[i]) + (a_plus * w1[i] * x1[i][current_time - 1] * y_fire_pattern)
        w1[i] = w1[i] + delta_w
        if w1[i] <0 :
            w1[i]=0.1
        # if i ==0 :
        #     print (w1)

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
        delta_w = (-a_minus * w2[i] * y2[i][current_time - 1] * fire_pattern[i]) + (a_plus * w2[i] * x2[i][current_time - 1] * y_fire_pattern)
        w2[i] = w2[i] + delta_w
        if w2[i] <0 :
            w2[i]=0.1

fig = figure(num=None, figsize=(20, 10))
subplot(211)
plot(output1.timer, output1.u)
ylabel('U')
xlabel('Time')
title('output1')
grid(True)

subplot(212)
plot(output2.timer, output2.u)
ylabel('U')
xlabel('Time')
title('output2')
grid(True)
show()

print("==")
print (w1)
print (w2)
plot(w1)
plot(w2)
show()