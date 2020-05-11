import random
import matplotlib.patches as mpatches
from project2.Neuron import Neuron
from project2.Neuron import Random_input
from matplotlib.pyplot import *

excitatory_N1 = 5
excitatory_N2 = 5
inhibitory_N = 5
N = excitatory_N1 + excitatory_N2 + inhibitory_N

group = []
w = []

c = 0
for i in range(inhibitory_N):
    group.append(Neuron(type="inh", index=c, group=1))
    c += 1
for i in range(excitatory_N1):
    group.append(Neuron(type="exc", index=c, group=2))
    c += 1
for i in range(excitatory_N2):
    group.append(Neuron(type="exc", index=c, group=3))
    c += 1

w = [[0 for x in range(N)] for y in range(N)]

for i in range(inhibitory_N):
    for j in range(inhibitory_N):
        if i != j:
            # w[i][j] = random.random()
            w[i][j] = 2
for i in range(inhibitory_N, inhibitory_N + excitatory_N1):
    for j in range(inhibitory_N, inhibitory_N + excitatory_N1):
        if i != j:
            # w[i][j] = random.random()
            w[i][j] = 3
for i in range(inhibitory_N + excitatory_N1, inhibitory_N + excitatory_N1 + excitatory_N2):
    for j in range(inhibitory_N + excitatory_N1, inhibitory_N + excitatory_N1 + excitatory_N2):
        if i != j:
            # w[i][j] = random.random()
            w[i][j] = 2

# w[excitatory_N1][0] = random.random()
# w[0][excitatory_N1] = random.random()
w[excitatory_N1][0] = 4
w[0][excitatory_N1] = 4

# w[excitatory_N1 + excitatory_N2][0] = random.random()
# w[0][excitatory_N1 + excitatory_N2] = random.random()
w[excitatory_N1 + excitatory_N2][0] = 4
w[0][excitatory_N1 + excitatory_N2] = 4

for i in w:
    s = ""
    for j in i:
        s = s + " " + str(j)
    print(s)


y = [[-1 for x in range(N)] for y in range(len(group[0].timer))]
yi = [0] * len(group[0].timer)
x = group[0].timer

Input_i = 10

i_gen = Random_input(i=Input_i, step=100)

for i in range(len(group[0].timer)):
    print(round(i / len(group[0].timer), 4) * 100, "%")
    # # switch for fade input
    current_i = i_gen.get(i)
    # current_i = 0
    # if i < 100:
    #     current_i = i_gen.get(i)

    yi[i] = current_i

    for g in group:
        if g.type == "inh":
            current_i = 0.4
        if g.group == 2:
            current_i *=1.02
        result = g.update(j=i, input=current_i)
        if result > 0:
            y[i][g.index] = g.index
            for k in range(N):
                g.update_u(w[g.index][k] * result, j=i)

# # plotting

list1 = []
for i in range(len(group[0].timer)):
    for g in range(N):
        if y[i][g] != -1:
            list1.append((group[0].timer[i], y[i][g]))
if len(list1) == 0:
    print("Not single Neurons Fired!")
    exit()
cdict = {1: 'red', 2: 'blue', 3: "green"}
color = []
fig = figure(num=None, figsize=(20, 20))
fig.suptitle('Population of ' + str(excitatory_N1)+" ,"+str(excitatory_N2) + " Excitatory Neurons and " + str(inhibitory_N) + " Inhibitory Neurons", fontsize=14,
             fontweight='bold')
ax = subplot(211)
list1 = list(zip(*list1))

c = []
for y in list(list1[1]):
    if y < inhibitory_N:
        c.append("g")
    if inhibitory_N <= y < excitatory_N1 + inhibitory_N:
        c.append("r")
    if y >= inhibitory_N + excitatory_N1:
        c.append("b")

scatter(list(list1[0]), list(list1[1]), c=c, s=0.6)
ylabel('index')
xlabel('Time')
title('index-Time plot')
red_patch = mpatches.Patch(color='red', label='Excitatory Neuron Group 1')
green_patch = mpatches.Patch(color='green', label='Excitatory Neuron Group 2')
blue_patch = mpatches.Patch(color='blue', label='Inhibitory Neuron')
legend(handles=[red_patch, blue_patch, green_patch])
ax.set_xlim(xmin=0, xmax=group[0].time)
grid(True)

ax = subplot(212)
plot(group[0].timer, yi)
ylabel('input i')
xlabel('Time')
title('I-Time plot')
ax.set_xlim(xmin=0, xmax=group[0].time)
grid(True)
# savefig('../figures/' + 'Population of ' + str(excitatory_N1) +" ,"+str(excitatory_N2) +  " Excitatory Neurons and " + str(
#     inhibitory_N) + " Inhibitory Neurons  fixed Connection2" + '.png')
show()
