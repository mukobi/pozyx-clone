
class userInput:

    g = float(g_input.get())
    mass = float(mass_input.get())
    Fg = g * mass
    rho = 1.225
    xSectionArea = float(xSectionArea_input.get())
    firstRow = float(firstRow_input.get())
    lastRow = float(lastRow_input.get())
    rows = slice(firstRow, lastRow, 1)

class physicalLaws:
    pass

