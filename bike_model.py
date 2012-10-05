from math import sin
from numpy import deg2rad, mean, diff, abs
from collections import namedtuple
from pylab import plot, legend, xlabel, ylabel, show

class Chap:
    def __init__ (self, name, mass, width, height, initial_v=0):
        self.mass = mass
        self.height = height
        self.width = width
        self.v = [initial_v]
        self.name = name

    def __str__ (self):
        return self.name

##People
chaps = [Chap("David", 85.7, 0.7, 2),
         Chap("Joe", 90, 0.65, 2), 
         Chap("James", 120, 1, 2)]

## Constants
tor = 0.1 #s
slope = deg2rad(10) #degrees
G = 9.81
Cd = 1
rho = 1.2
rolling_R = 0.003

def drag (chap):
    air_drag = 0.5*rho * Cd * chap.v[-1]**2 * chap.width*chap.height
    rolling_drag = rolling_R * chap.mass * G
    return air_drag + rolling_drag

def force (chap):
        return chap.mass * G * sin(slope)

def steady_state (chap, npts=10, eps=0.0001):
    if type(chap) == list:
        return all(steady_state(chap, npts, eps) for chap in chaps)
    elif len(chap.v) < npts:
        return False
    else:
        return mean(abs(diff(chap.v[-npts:]))) < eps

while not steady_state(chaps):
    for chap in chaps:
        chap.v += [chap.v[-1] + tor * ((force(chap) - drag(chap))/chap.mass)]

t = [tor * i for i in range(len(chaps[0].v))]

for chap in chaps:
    plot(t, chap.v, label=str(chap))

legend(loc='best')
xlabel('Time (s)')
ylabel('Speed (m/s)')
show()
