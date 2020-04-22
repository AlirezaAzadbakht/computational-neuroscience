import numpy as np
from matplotlib.pyplot import *

TIME = 100
I_Time_Interval = [20,70]
STEPS = 0.125
U_REST = 0
R = 1
C = 10
I = 5

THRESHOLD = 2

timer = np.arange(0, TIME+STEPS, STEPS)
input_i = [0]*len(timer)
for i in range(len(input_i)):
    if timer[i] > I_Time_Interval[0] and timer[i] < I_Time_Interval[1]:
        input_i[i] = I
tm = R*C
u = [U_REST]*len(timer)
dt = STEPS

for i in range(len(timer)):
    u[i] = u[i-1] + (-u[i-1] + R*input_i[i]) / tm*dt
    if u[i] >= THRESHOLD:
        u[i] = U_REST

fig = figure(num=None, figsize=(20, 10))
fig.suptitle('Leaky Integrate-and-Fire\n\n'+"R: "+str(R)+"    C: "+str(C)+"    I: "+str(I)+"    THRESHold: "+str(THRESHOLD), fontsize=14, fontweight='bold')
subplot(221)
plot(timer, u)
ylabel('U')
xlabel('Time')
title('U-Time plot')
grid(True)

subplot(222)
plot(timer, input_i)
ylabel('I')
xlabel('Time')
title('I-Time plot')
grid(True)

show()