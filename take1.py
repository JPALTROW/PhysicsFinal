from vpython import *
import random
n=3

MASS = 1
DISTANCE = 2
EQUILIBRIUM = 1
G = 9.81
k = 1

endpoints = []
boxes = []
velocities = []
forces = []

dt = .001

def init():
    for e in range(n):
        boxes.append(box(pos = vector(6,10-e*DISTANCE-DISTANCE/2,0), size = vector(DISTANCE,1,1), color = vector(random.random(), random.random(), random.random())))
        velocities.append(vector(0,0,0))
        forces.append(vector(0, 0, 0))

def move():
    for e in range(n):
        boxes[e].pos+=velocities[e] * dt
        velocities[e]+=forces[e]/MASS * dt
    update_forces()

def update_forces():
    for i in range(n):
        forces[i] = vector(0, 0, 0)
    for i in range(n-1):
        diff = boxes[i+1].pos - boxes[i].pos
        diff = (diff.mag - EQUILIBRIUM) / diff.mag * diff
        forces[i] += diff*k
        forces[i+1] += diff*(-k)

init()

i = 0
while(i < 1000):
    rate(1/dt)
    move()
