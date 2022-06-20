# Base units cm, g
import numpy as np

UNITS = {
    "m": 100,
    "cm": 1,
    "mm": 0.1,
    "kg": 1,
    "g": 0.001,
}

def velocity(vel, distance):
    if distance in UNITS:
        return vel * UNITS[distance]
    return -1

def acceleration(acel, distance):
    if distance in UNITS:
        return acel * UNITS[distance]
    return -1

def density(density, weight, distance): # kg / cm^2
    if weight in UNITS and distance in UNITS:
        return density * UNITS[weight] / (UNITS[distance]**3)
    return -1

def torque(torq, weight, distance): # kg * m^2 / s^2
    if weight in UNITS and distance in UNITS:
        return torq * UNITS[weight] * UNITS[distance] * UNITS[distance]
    return -1

def coordinate(coord, distance):
    if distance in UNITS and len(coord) == 2:
        return (coord[0] * UNITS[distance], coord[1] * UNITS[distance])
    return -1

def vertices(vertices, distance):
    return [(vertex[0] * UNITS[distance], vertex[1] * UNITS[distance]) for vertex in vertices]

def densityFromMass(mass, vertices, weight, distance): # kg / cm^2
    if weight in UNITS and distance in UNITS:
        area = areaFromVertices(vertices)
        return mass * UNITS[weight] / (area * (UNITS[distance]**2))
    return -1

def areaFromVertices(vertices):
    x = []
    y = []
    for vertex in vertices:
        x.append(vertex[0])
        y.append(vertex[1])
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))