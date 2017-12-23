"""
class phys_props:

    def __init__ (self, xSectionArea, airDensity, mass, gravity):
        self.xSectionArea = xSectionArea
        self.airDensity = airDensity
        self.mass = mass
        self.gravity = gravity
        self.gravityForce = mass * gravity
"""
class redBall:
        xSectionArea = 0.007696812625395605
        airDensity = 1.225
        mass = 0.033    # kg
        g = -9.81
        Fg = mass * gravity

class orangeBall:
        xSectionArea = 0.03208762596411475
        airDensity = 1.225
        mass = 0.327    # kg
        g = -9.81
        gravityForce = mass * gravity

class yellowBall:
        xSectionArea = 0.017954667017554445
        airDensity = 1.225
        mass = 0.327    # kg
        g = -9.81
        Fg = mass * gravity

class blueBall:
        xSectionArea = 0.03259493234522017
        airDensity = 1.225
        mass = 0.112    # kg
        g = -9.81
        Fg = mass * gravity

