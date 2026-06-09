from gamepad import GamepadSofaController, GamepadCallbacks
import numpy as np


def createScene(rootnode):

    rootnode.addObject("DefaultAnimationLoop")
    rootnode.addObject("InteractiveCamera", position=[0, 0, 10], lookAt=[0, 0, 0])

    rootnode.addObject('RequiredPlugin', pluginName=['Sofa.Component.LinearSolver.Iterative' # Needed to use components [CGLinearSolver]  
                                                    ,'Sofa.Component.Mass' # Needed to use components [UniformMass]  
                                                    ,'Sofa.Component.ODESolver.Backward' # Needed to use components [EulerImplicitSolver]  
                                                    ,'Sofa.Component.SolidMechanics.Spring' # Needed to use components [RestShapeSpringsForceField]  
                                                    ,'Sofa.Component.StateContainer' # Needed to use components [MechanicalObject]  
                                                    ,'Sofa.Component.Visual']) # Needed to use components [InteractiveCamera]  

    # Create a simple scene with a single frame that we will move with the gamepad input. 
    simulation = rootnode.addChild("Simulation")
    simulation.addObject("EulerImplicitSolver")
    simulation.addObject("CGLinearSolver", iterations=50, tolerance=1e-5, threshold=1e-5)
    frame = simulation.addChild("Frame")
    frame.bbox.value = [[-10, -10, -10], [10, 10, 10]]
    frame.addObject("MechanicalObject", template="Rigid3", showObject=True, showObjectScale=1)
    frame.addObject("UniformMass", totalMass=1)
    frame.addObject("RestShapeSpringsForceField", stiffness=1000) # Add a spring force field to keep the frame in its rest position.
    # We will update the rest position of the spring force field with the gamepad input to move the frame.

    # The left stick will move the frame in the horizontal plane (x and z axes), 
    # while the right stick will move it vertically (y axis). We also define a button to invert the axis of the sticks.
    scale = 0.01 # Scale factor to control the sensitivity of the gamepad input (adjust as needed)

    def moveFrameXZ(horizontal, vertical):
        position = frame.getMechanicalState().rest_position.value[0]
        position = position + np.array([scale * horizontal, 0, scale * vertical, 0, 0, 0, 1])
        frame.getMechanicalState().rest_position.value = [position]

    def moveFrameY(_, vertical):
        position = frame.getMechanicalState().rest_position.value[0]
        position = position + np.array([0, scale * vertical, 0, 0, 0, 0, 1])
        frame.getMechanicalState().rest_position.value = [position]

    def invertAxis():
        # This is an example of a shared variable.
        # Click the a button to invert the axis of the sticks.
        nonlocal scale
        scale = -scale

    callbacks = GamepadCallbacks()
    callbacks.sticks.left.moved = moveFrameXZ
    callbacks.sticks.right.moved = moveFrameY
    callbacks.buttons.south.released = invertAxis
    rootnode.addObject(GamepadSofaController(callbacks=callbacks))