from vpython import *
import random
n=6


MASS = 1
DISTANCE = 6
EQUILIBRIUM = 4
G = 9.81
k = 4
DAMPEN = .1

endpoints = []
boxes = []
velocities = []
forces = []

dt = .001

def init():
    for e in range(n):
        boxes.append(sphere(pos = vector(10-e*DISTANCE,6,0), radius = .5, color = vector(random.random(), random.random(), random.random())))
        velocities.append(vector(0,0,0))
        forces.append(vector(0, 0, 0))

def move():
    for e in range(n):
        boxes[e].pos+=velocities[e] * dt
        velocities[e]+=forces[e]/MASS * dt
    update_forces()

def update_forces():
    for i in range(n):
        forces[i] = vector(0, -G*MASS, 0)
    for i in range(n-1):
        diff = (boxes[i+1].pos + boxes[i].pos)/2 - boxes[i].pos
        diff = (diff.mag - EQUILIBRIUM/2) / diff.mag * diff
        forces[i] += diff*k
        forces[i+1] += diff*(-k)
    forces[0] = vector(0,0,0)
    forces[n-1] = vector(0,0,0)
    for i in range(n):
        forces[i] += DAMPEN*(velocities[i].dot(velocities[i]))*(-1)*velocities[i].hat

init()

i = 0
while(i < 1000):
    rate(1/dt)
    move()
