import numpy as np
import random


class Neuron:
    def __init__(self, type="exc", index=0, group = 0):  # exc/inh
        self.group = group
        self.index = index
        self.type = type
        self.time = 700
        self.steps = 0.25
        self.u_rest = 0
        self.r = 10
        self.c = 5
        self.threshold = 1+ random.random() * 2

        self.timer = np.arange(0, self.time + self.steps, self.steps)
        self.tm = self.r * self.c
        self.dt = self.steps
        self.i_input = 0
        self.u = [self.u_rest] * len(self.timer)

    def update(self, j, input):
        self.u[j] += self.u[j - 1] + (-self.u[j - 1] + self.r * input) / self.tm * self.dt
        result = 0
        if self.u[j] >= self.threshold:
            result = self.threshold - self.u_rest
            self.u[j] = self.u_rest
        return result

