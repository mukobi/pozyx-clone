"""
class phys_props:

    def __init__ (self, xSectionArea, airDensity, mass, gravity):
        self.xSectionArea = xSectionArea
        self.airDensity = airDensity
        self.mass = mass
        self.gravity = gravity
        self.gravityForce = mass * gravity
"""
from math import pi
import pandas as pd

airDensity = 1.225
g = -9.81

# drag model function

class Ball:
    def __init__(self, circumference=1, mass=1, xsec=1):

        self.circumference = circumference
        self.mass = mass

        self.xDF = pd.DataFrame()
        self.vDF = pd.DataFrame()
        self.aDF = pd.DataFrame()
        self.experienceList = []

        self.diameter = self.circumference / pi # diameter of ball in meters
        self.radius = 1/2 * self.diameter * 0.01
        self.xSectionArea = pi*self.radius**2    # cross sectional area in meters        
        #xSectionArea = 0.007796125309884948
        self.Fg = mass * g

    def loadData(self, filename, trajectoryType='throw'):
        self.xdataDF = pd.read_csv(filename)

    def __str__(self):
        return "ball properties: radius={}, mass={}, xsec={}".format(self.radius, self.mass, self.xSectionArea)

    # fitting function

    # add Model


class ColoredBall(Ball):

    def __init__(self, color='white'):
        Ball.__init__(self)
        self.color = color

    def __str__(self):
        return Ball.__str__(self) + " color={}".format(self.color)


class redBall:
    circumference = 31.3
    diameter = circumference / pi # diameter of ball in meters
    radius = 1/2 * diameter * 0.01
    xSectionArea = pi*radius**2    # cross sectional area in meters        
    #xSectionArea = 0.007796125309884948
    airDensity = 1.225
    mass = 0.033
    g = -9.81
    Fg = mass * g

#import pdb; pdb.set_trace()
###############################################################################33

class redBall():
    from math import pi
    circumference = 31.3
    diameter = circumference / pi # diameter of ball in meters
    radius = 1/2 * diameter * 0.01
    xSectionArea = pi*radius**2    # cross sectional area in meters        
    #xSectionArea = 0.007796125309884948
    airDensity = 1.225
    mass = 0.033
    g = -9.81
    Fg = mass * g

class orangeBall:
    from math import pi
    circumference = 63.5
    diameter = circumference / pi # diameter of ball in meters
    radius = 1/2 * diameter * 0.01
    xSectionArea = pi*radius**2    # cross sectional area in meters        
    #xSectionArea = 0.03208762596411475
    airDensity = 1.225
    mass = 0.327    # kg
    g = -9.81
    Fg = mass * g

class yellowBall:
    from math import pi
    circumference = 47.5
    diameter = circumference / pi # diameter of ball in meters
    radius = 1/2 * diameter * 0.01
    xSectionArea = pi*radius**2    # cross sectional area in meters        
    #xSectionArea = 0.017954667017554445
    airDensity = 1.225
    mass = 107*0.001    # kg
    g = -9.81
    Fg = mass * g

class blueBall:
    from math import pi
    circumference = 64
    diameter = circumference / pi # diameter of ball in meters
    radius = 1/2 * diameter * 0.01
    xSectionArea = pi*radius**2    # cross sectional area in meters
    #xSectionArea = 0.03259493234522017
    airDensity = 1.225
    mass = 0.112    # kg
    g = -9.81
    Fg = mass * g

class rocket:
    from math import pi
    circumference = 70.38
    diameter = circumference / pi # diameter of ball in meters
    radius = 1/2 * diameter * 0.01
    xSectionArea = pi*radius**2    # cross sectional area in meters        
    #xSectionArea = 0.003940255
    airDensity = 1.225
    mass = 0.225    # kg
    g = -9.81
    Fg = mass * g

