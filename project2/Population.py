import random
import matplotlib.patches as mpatches
from project2.Neuron import Neuron
from project2.Neuron import Random_input
from matplotlib.pyplot import *

excitatory_N = 800
inhibitory_N = 200
N = excitatory_N + inhibitory_N

group = []
w = []

c = 0
for i in range(inhibitory_N):
    group.append(Neuron(type="inh", index=c))
    c += 1
for i in range(excitatory_N):
    group.append(Neuron(type="exc", index=c))
    c += 1

for i in range(N):
    temp = []
    for j in range(N):
        if i == j:
            temp.append(0)
        else:
            temp.append(random.random())
            # temp.append(1)
    w.append(temp)

y = [[-1 for x in range(N)] for y in range(len(group[0].timer))]
yi = [0] * len(group[0].timer)
x = group[0].timer

i_gen = Random_input(i=1, step=100)

for i in range(len(group[0].timer)):
    current_i = i_gen.get(i)
    yi[i] = current_i
    for g in group:
        result = g.update(j=i, input=current_i)
        if result > 0:
            y[i][g.index] = g.index
            for k in range(N):
                g.update_u(w[g.index][k] * result, j=i)

list1 = []
for i in range(len(group[0].timer)):
    for g in range(N):
        if y[i][g] != -1:
            list1.append((group[0].timer[i], y[i][g]))

# plotting
cdict = {1: 'red', 2: 'blue'}
color = []
fig = figure(num=None, figsize=(20, 20))
fig.suptitle('Population of ' + str(excitatory_N) + " Excitatory Neurons and " + str(inhibitory_N) + " Inhibitory Neurons", fontsize=14,
             fontweight='bold')
ax = subplot(211)
list1 = list(zip(*list1))
c = ["b" if y >= excitatory_N else "r" for y in list(list1[1])]
scatter(list(list1[0]), list(list1[1]), c=c, s=0.6)
ylabel('index')
xlabel('Time')
title('index-Time plot')
red_patch = mpatches.Patch(color='red', label='Excitatory Neuron')
blue_patch = mpatches.Patch(color='blue', label='Inhibitory Neuron')
legend(handles=[red_patch, blue_patch])
ax.set_xlim(xmin=0)
grid(True)

subplot(212)
plot(group[0].timer, yi)
ylabel('input i')
xlabel('Time')
title('I-Time plot')
grid(True)
savefig('../figures/population of random connection2.png')
show()
