from vpython import *
import random

n=20

MASS = 1
DISTANCE = 6
EQUILIBRIUM = 4
G = 9.81
k = 10
DAMPEN = .01

masses = [1]*n
masses[14] = 20
endpoints = []
boxes = []
velocities = []
forces = []

dt = .001

def init():
    for e in range(n):
        boxes.append(sphere(pos = vector(10-e*DISTANCE,6,0), radius = 2, color = vector(0,1,0)))
        velocities.append(vector(0,0,0))
        forces.append(vector(0, 0, 0))
    boxes[14].color = vector(1,0,0)

def move():
    for e in range(n):
        boxes[e].pos+=velocities[e] * dt
        velocities[e]+=forces[e]/MASS * dt
    update_forces()

def update_forces():
    for i in range(n):
        forces[i] = vector(0, -G*masses[i], 0)
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
