from vpython import *
n=3
MASS = 1
endpoints = []
velocities = []
forces = []


def move(endpoints, velocities, forces):
    for e in range(n):
        endpoints[e]+=velocities[e]
        velocities[e]+=forces[e]/MASS
    update_forces(edpoints, velocities, forces)

def update_forces(edpoints, velocities, forces):
    
