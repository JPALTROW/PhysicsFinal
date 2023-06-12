from vpython import *

#very IMPORTANT VARIABLES
n = 20 #number of ballz
dt = .001 #time constant
setup = True
trailing = False

#TEN MILLION ARRAYS
spvings = [] #array of spvings (contains helix objects)
masses = [1]*n #array of masses (stores constant values corresponding to mass)
balls = [] #array of balls (contains sphere objects)
velocities = [] #array of velocities for each ball
forces = [] #array of forces applied on each ball
energyB = [] #stores energies of each ball (energyB[i]=[Kinetic energy of i, Potential energy of i])
energyS = [] #stores energy of each spring (elastic)

#PHYSICAL CONSTANTS
DISTANCE = 6 #original distance between each spving
EQUILIBRIUM = 4 #equilibrium distance between each spving
G = 9.81 #gravity
k = 100 #spring constant
DAMPEN = .01 #dampening constant

wt = wtext(text='Mass for ball ') #text

l = [] #list of choices for masselector
for i in range(n):
    l.append(str(i)) #add all numbers

#dropdown menu, lets you pick which ball's mass to edit
def massmenu(m):
    slidinator.value = masses[masselector.index] #ensure fast update of mass
    massval.text = ' = ' + str(masses[masselector.index]) #display mass
masselector = menu(choices=l, index=0, bind=massmenu, text='Mass of ball')

massval = wtext(text=' = ' + str(masses[masselector.index])) #text


#allows you to edit the mass of the selected ball
def selectmass(s):
    masses[masselector.index] = s.value
    massval.text = ' = ' + str(masses[masselector.index])
    slidinator.value = masses[masselector.index]
slidinator = slider(min=1, max=10, value=1, length=220, bind=selectmass)

scene.append_to_caption('\n\n')
bt = wtext(text='Number of ballz = ' + str(n)) #text

#slider to pick # of ballz
def selectballz(s):
    global n
    global masses
    n = int(s.value) #integer number of ballz
    l = [] #ensuring masselector updates to account for appropriate # of balls
    for i in range(n):
        l.append(str(i))
    bt.text='Number of ballz = ' + str(n) #text
    masses = [1]*n #initialize masses array
    masselector.index=0 #niceity
    masselector.choices=l #ensuring masselector updates to account for appropriate # of balls
    slidinator.value=masses[masselector.index] #niceity
ballzelector=slider(min=1, max=100, value=20, length=220, bind=selectballz)

scene.append_to_caption('\n\n')
kt = wtext(text = 'Spving konstant = ' + str(k))
def selectspvingkonstant(s):
    global k
    k = s.value
    kt.text = 'Spving konstant = ' + str(k)
spvingkonstantsevector=slider(min=1, max=200, value=100, length=220, bind=selectspvingkonstant)
'''
void begin(b)
Inputs:
Returns:
Button updates to change state from setup to simulation
'''
def begin(b):
    global setup
    setup = not setup
    if setup:
        b.text = 'Begin'
    else:
        b.delete()
scene.append_to_caption('\n\n')
bb = button(text='Begin', bind=begin) #begin button

'''
void trail(b)
Inputs:
Returns:
Toggles trace on the balls (optional feature)
'''
def trail(b):
    global trailing
    trailing = not trailing #toggle
    if trailing:
        b.text = 'Trail Off'
        for i in balls:
            i.make_trail = True
    else:
        b.text = 'Trail On'
        for i in balls:
            i.make_trail = False
            i.clear_trail() #no more trail :(
tb = button(text='Trail On', bind=trail)

'''
void init()
Inputs:
Returns:
initializes balls based on DISTANCE and initializes spvings and energy arrays
'''
def init():
    for e in range(n):
        t = (masses[e] - slidinator.min)/(slidinator.max-slidinator.min) #color gradient based on mass
        balls.append(sphere(pos = vector(10-e*DISTANCE,6,0), radius = 2, color = vector(0,1,1) * (1-t) + vector(1,0,1) * t, make_trail = False, retain = 100)) #creates masses
        velocities.append(vector(0,0,0)) #initialize velocity to 0
        forces.append(vector(0, 0, 0)) #initialize force to 0
        energyB.append([0,masses[e]*G*balls[e].pos.y]) #initialize gravitational potential energy
    for e in range(n-1):
        spvings.append(helix(pos=balls[e].pos, axis=balls[e+1].pos-balls[e].pos, thickness=1)) #draw springs
        energyS.append(1/2 * k * ((balls[e].pos-balls[e+1].pos).mag-EQUILIBRIUM)**2) #initialize elastic potential energy
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
applies acceleration (force/mass) to velocity and velocity to position to create simulation
redraws springs in correct location
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
        forces[i] = vector(0, -G*masses[i], 0) #gravitational force
    for i in range(n-1):
        diff = (balls[i+1].pos + balls[i].pos)/2 - balls[i].pos
        diff = (2*diff.mag - EQUILIBRIUM) / diff.mag * diff
        forces[i] += diff*k #spring force on each end
        forces[i+1] += diff*(-k)
    forces[0] = vector(0,0,0) #endpoints should not move
    forces[n-1] = vector(0,0,0)
    for i in range(n):
        forces[i] += DAMPEN*(velocities[i].dot(velocities[i]))*(-1)*velocities[i].hat #velocity squared dampening

'''
void update_energies()
Inputs:
Returns:
updates energies arrays based on physical scenario
'''
def update_energies():
    for i in range(n):
        energyB[i] = [masses[i]*velocities[i].mag*velocities[i].mag/2,masses[i]*G*balls[i].pos.y] #kinetic, gravitational potential energy
    for i in range(n-1):
        energyS[i] = 1/2 * k * ((balls[i].pos-balls[i+1].pos).mag-EQUILIBRIUM)**2 #elastic potential energy

while(setup):
    rate(1/dt)
    #stall while setting up :)

#GRAPH DEFINITIONS
energy = graph(title='Energies of the Spvingz', xtitle='Time (ms)', ytitle='Energy (J)', fast=True, width=800)
total = gcurve(color = vector(1,0,1), label='Total Energy') # a graphics curve
potential = gcurve(color = vector(0,0,1), label='Potential Energy')
kinetic = gcurve(color = vector(0,1,1), label='Kinetic Energy')

init()
sleep(1) #Yay this is very important
slidinator.delete() #clearing setup screen
masselector.delete() #clearing setup screen
ballzelector.delete() #clearing setup screen
spvingkonstantsevector.delete()
wt.text = '' #clearing setup screen
bt.text = '' #clearing setup screen
kt.text = ''

massval.text = '' #clearing setup screen

i = 0 #i is how many seconds have passed, we love sensible variable names
while(True): #run function
    rate(1/dt) #run the loop (also strangely very important)
    energyP = 0
    energyK = 0
    energyT = 0
#calculate energies
    for j in range(n):
        energyP += energyB[j][1]
        energyK += energyB[j][0]
    for j in range(n-1):
        energyP += energyS[j]
    energyT = energyP + energyK
#graph
    total.plot(i,energyT)
    potential.plot(i, energyP)
    kinetic.plot(i,energyK)

    move()
    i+=1
