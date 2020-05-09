import numpy as np
import random


class Neuron:
    def __init__(self, type="exc", index=0):  # exc/inh
        self.index = index
        self.type = type
        self.time = 50
        self.steps = 0.25
        self.u_rest = 0
        self.r = 10
        self.c = 5
        self.threshold = 2 + random.random() * 2

        self.timer = np.arange(0, self.time + self.steps, self.steps)
        self.tm = self.r * self.c
        self.dt = self.steps
        self.i_input = 0
        self.u = [self.u_rest] * len(self.timer)

    def update(self, j, input):
        self.u[j] = self.u[j - 1] + (-self.u[j - 1] + self.r * input) / self.tm * self.dt
        result = 0
        if self.u[j] >= self.threshold or self.u[j] < self.u_rest:
            result = self.threshold - self.u_rest
            self.u[j] = self.u_rest
            #print("fire :", self.type, self.index, result)
        return result

    def update_u(self, value, j):
        if type == "exc":
            self.u[j] += value
        else:
            self.u[j] -= value


class Random_input:
    def __init__(self, i=5, step=20):
        self.last_i = 0
        self.going_up = True
        self.i = i
        self.step = step

    def get(self, iterate):
        if iterate % 20 == 0:
            self.going_up = not self.going_up
        temp = random.random()
        if self.going_up:
            temp = self.last_i + temp * (self.i / 2)
        else:
            temp = self.last_i - temp * (self.i / 2)
        if temp > self.i * 2 or temp <0:
            temp = random.random() * (self.i)
        self.last_i = temp
        return temp
