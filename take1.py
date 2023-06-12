from vpython import *

n = 20 #number of ballz
dt = .001 #time constant
setup = True
trailing = False

spvings = [] #array of spvings (contains helix objects)
masses = [1]*n #array of masses (stores constant values corresponding to mass)
balls = [] #array of balls (contains sphere objects)
velocities = [] #array of velocities for each ball
forces = [] #array of forces applied on each ball
energyB = [] #stores energies of each ball (energyB[i]=[Kinetic energy of i, Potential energy of i])
energyS = [] #stores energy of each spring (elastic)

wt = wtext(text='Mass for ball ') #text dwai

def massmenu(m):
    slidinator.value = masses[masselector.index] #ensure fast update
    massval.text = ' = ' + str(masses[masselector.index]) #display mass

l = [] #list of choices for masselector
for i in range(n):
    l.append(str(i)) #UGGG VPYTHON

masselector = menu(choices=l, index=0, bind=massmenu, text='Mass of ball')
#dropdown menu, lets you pick which ball's mass to edit

massval = wtext(text=' = ' + str(masses[masselector.index])) #text dwai

def selectmass(s):
    masses[masselector.index] = s.value
    massval.text = ' = ' + str(masses[masselector.index])
    slidinator.value = masses[masselector.index]

slidinator = slider(min=1, max=10, value=1, length=220, bind=selectmass)
#allows you to edit the mass of the selected ball

bt = wtext(text='# of ballz = ' + str(n)) #text dwai

def selectballz(s):
    global n #****ing python
    global masses #****ing python
    n = int(s.value)
    l = [] #ensuring masselector updates to account for appropriate # of balls
    for i in range(n): #^
        l.append(str(i)) #^
    bt.text='Number of ballz = ' + str(n) #text dwai
    masses = [1]*n
    masselector.index=0 #niceity
    masselector.choices=l #ensuring masselector updates to account for appropriate # of balls
    slidinator.value=masses[masselector.index] #niceity

ballzelector=slider(min=1, max=100, value=20, length=220, bind=selectballz) #slider to pick # of ballz

'''
void begin(b)
Inputs:
Returns:
pause button updates global setup variable
'''
def begin(b):
    global setup
    setup = not setup
    if setup:
        b.text = 'Begin'
    else:
        b.delete()

bb = button(text='Begin', bind=begin) #begin button

'''
void trail(b)
Inputs:
Returns:
Toggles trace on the balls
'''
def trail(b):
    global trailing
    trailing = not trailing
    if trailing:
        b.text = 'Trail Off'
        for i in balls:
            i.make_trail = True
    else:
        b.text = 'Trail On'
        for i in balls:
            i.make_trail = False
            i.clear_trail()

tb = button(text='Trail On', bind=trail)

'''
void init()
Inputs:
Returns:
initializes balls based on DISTANCE and initializes spvings and energy arrays
'''
def init():
    for e in range(n):
        t = (masses[e] - slidinator.min)/(slidinator.max-slidinator.min)
        balls.append(sphere(pos = vector(10-e*DISTANCE,6,0), radius = 2, color = vector(0,1,1) * (1-t) + vector(1,0,1) * t, make_trail = False, retain = 100))
        velocities.append(vector(0,0,0))
        forces.append(vector(0, 0, 0))
        energyB.append([0,masses[e]*G*balls[e].pos.y])
    for e in range(n-1):
        spvings.append(helix(pos=balls[e].pos, axis=balls[e+1].pos-balls[e].pos, thickness=1))
        energyS.append(1/2 * k * ((balls[e].pos-balls[e+1].pos).mag-EQUILIBRIUM)**2)
    energy = graph(title='Energies of the Spvingz', xtitle='Time (s)', ytitle='Energy (J)', fast=True, width=800)
    total = gcurve(color = vector(1,0,1), label='Total Energy') # a graphics curve
    potential = gcurve(color = vector(0,0,1), label='Potential Energy')
    kinetic = gcurve(color = vector(0,1,1), label='Kinetic Energy')

'''
void move()
Inputs:
Returns:
updates positions and velocities of balls and redraws springs based on velocities and forces

move() is the only function we will be running, calls update_forces after updating position
'''
def move():
    for e in range(n):
        balls[e].pos+=velocities[e] * dt
        velocities[e]+=forces[e]/masses[e] * dt
    for e in range(n-1):
        spvings[e].pos = balls[e].pos
        spvings[e].axis = balls[e+1].pos-balls[e].pos
    update_forces()
    update_energies()

'''
void update_forces()
Inputs:
Returns:
updates forces array based on gravity and spring force
'''
def update_forces():
    for i in range(n):
        forces[i] = vector(0, -G*masses[i], 0)
    for i in range(n-1):
        diff = (balls[i+1].pos + balls[i].pos)/2 - balls[i].pos
        diff = (2*diff.mag - EQUILIBRIUM) / diff.mag * diff
        forces[i] += diff*k
        forces[i+1] += diff*(-k)
    forces[0] = vector(0,0,0)
    forces[n-1] = vector(0,0,0)
    for i in range(n):
        forces[i] += DAMPEN*(velocities[i].dot(velocities[i]))*(-1)*velocities[i].hat

'''
void update_energies()
Inputs:
Returns:
updates energies arrays based on physical scenario
'''
def update_energies():
    for i in range(n):
        energyB[i] = [masses[i]*velocities[i].mag*velocities[i].mag/2,masses[i]*G*balls[i].pos.y]
    for i in range(n-1):
        energyS[i] = 1/2 * k * ((balls[i].pos-balls[i+1].pos).mag-EQUILIBRIUM)**2

while(setup):
    rate(1/dt)
    #stall while setting up :)

#GRAPH DEFINITIONS
energy = graph(title='Energies of the Spvingz', xtitle='Time (ms)', ytitle='Energy (J)', fast=True, width=800)
total = gcurve(color = vector(1,0,1), label='Total Energy') # a graphics curve
potential = gcurve(color = vector(0,0,1), label='Potential Energy')
kinetic = gcurve(color = vector(0,1,1), label='Kinetic Energy')

#PHYSICAL CONSTANTS
DISTANCE = 6 #original distance between each spving
EQUILIBRIUM = 4 #equilibrium distance between each spving
G = 9.81 #gravity
k = 100 #spring constant
DAMPEN = .01 #dampening constant

init()
sleep(1) #****ing vpython
slidinator.delete() #clearing setup screen
masselector.delete() #clearing setup screen
ballzelector.delete() #clearing setup screen
wt.text = '' #clearing setup screen
bt.text = '' #clearing setup screen
massval.text = '' #clearing setup screen

i = 0 #i is how many seconds have passed, we love sensible variable names
while(True): #run function
    rate(1/dt)
    energyP = 0
    energyK = 0
    energyT = 0

    for j in range(n):
        energyP += energyB[j][1]
        energyK += energyB[j][0]
    for j in range(n-1):
        energyP += energyS[j]
    energyT = energyP + energyK

    total.plot(i,energyT)
    potential.plot(i, energyP)
    kinetic.plot(i,energyK)

    move()
    i+=1
