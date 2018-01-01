tk.Label(root,
         text="Set Modeling Scripts",
         fg = "black",
         font = "Times").pack()



def modelPosition():
    os.system('python3 model_position.py')

modelPositionButton=tk.Button(text="model position",command= modelPosition)
modelPositionButton.pack()

def modelVelocity():
    os.system('python3 model_velocity.py')

modelVelocityButton=tk.Button(text="model velocity",command= modelVelocity)
modelVelocityButton.pack()

def modelAcceleration():
    os.system('python3 model_acceleration.py')

modelAccelerationButton=tk.Button(text="model acceleration",command= modelAcceleration)
modelAccelerationButton.pack()

def modelDragForce():
    os.system('python3 model_dragForce.py')

modelDragButton = tk.Button(text='model drag force', command = modelDragForce)
modelDragButton.pack()

def fittingRoutine():
    os.system('python3 fitting_routine.py')

fittingRoutineButton = tk.Button(text='fitting routine', command = fittingRoutine)
fittingRoutineButton.pack()

fields = ('Annual Rate', 'Number of Payments', 'Loan Principle', 'Monthly Payment', 'Remaining Loan')
"""
