import Sofa

from inputs import devices

from threading import Thread, Lock
import queue
from .callbacks import GamepadCallbacks
from .state import GamepadState, GamepadType

import os
filename = "gamepad/" + os.path.basename(__file__)

def read_gamepad(gamepad, queue):
    """Continuously read gamepad events and put them in the queue for processing in the main thread.
    """
    import time
    while True:
        if gamepad is not None:
            events = gamepad.read()
            for event in events:
                if event.ev_type != "Sync": # It is a gamepad axis event: joysticks, triggers, d-pad
                    try:
                        queue.put_nowait(event)
                    except Exception as e:
                        pass  # If the queue is full, we simply discard the event to avoid blocking the thread
        else:
            Sofa.msg_warning(filename,"Gamepad disconnected.")
            time.sleep(2)
            gamepad = devices.gamepads[0] if devices.gamepads else None


class GamepadSofaController(Sofa.Core.Controller):
    """Sofa controller that reads input from a gamepad and updates the position of a target object accordingly.

    Parameters:
        callbacks: GamepadCallbacks = GamepadCallbacks()
            Callbacks for the different gamepad inputs (sticks, triggers, buttons) that will be called when the corresponding input is detected. 
            This allows to define custom behavior for each input in the scene, such as moving the target of a robot effector.
        index: int = 0
            Index of the gamepad to use if multiple gamepads are connected. By default, it uses the first gamepad detected (index 0).
    """

    def __init__(self, callbacks: GamepadCallbacks = GamepadCallbacks(), index: int = 0):
        
        super().__init__()
        self.gamepadState : GamepadState = None
        self.gamepad = None
        self.callbacks = callbacks
        
        Sofa.msg_info(filename, "Getting gamepads...")
        if devices.gamepads:
            Sofa.msg_info(filename, f"Gamepad detected: {devices.gamepads[0].name}")

            if len(devices.gamepads) >= index - 1:
                self.gamepad = devices.gamepads[index]
                self.gamepadState = GamepadType.get_gamepad_class(gamepad_name=self.gamepad.name)() # Initialize the gamepad state based on the type of gamepad detected

                self._events = queue.Queue(0)  # Queue to hold gamepad events
                self.lock = Lock()  # Lock for thread safety
                self._thread = Thread(target=read_gamepad, 
                                      args=[self.gamepad, self._events], 
                                      daemon=True)
                self._thread.start()
            else:
                Sofa.msg_error(filename, f"Size of detected gamepad list is {len(devices.gamepads)} while requested index is {index}.")

        else:
            Sofa.msg_warning(filename, "No gamepad detected.")
    
    def onAnimateBeginEvent(self, _):
        """Process gamepad events and update the target position and gripper state accordingly 
        at the beginning of each animation step.
        """

        if self.gamepad is None:
            return

        events_to_process = []
        if self.gamepad and not self._events.empty():
            events_to_process = list(self._events.queue.copy()) # Get a copy of the current events in the queue
            events_to_process = events_to_process[:] # Convert to a list to avoid issues with the queue being modified while processing
            self._events.queue.clear() # Clear the queue to avoid processing the same events multiple times

        previous_south_button = self.gamepadState.buttons.south
        previous_north_button = self.gamepadState.buttons.north
        previous_east_button = self.gamepadState.buttons.east
        previous_west_button = self.gamepadState.buttons.west

        for event in events_to_process:
            if event is None:
                continue
            
            # Update gamepad state based on the latest event
            self.gamepadState.update(event)
            
        # Based on the updated gamepad state, determine the target position and gripper state
        
        # Buttons
        ## Clicked (on released)
        if self.gamepadState.buttons.south == 0 and previous_south_button == 1: 
            if self.callbacks.buttons.clicked.south is not None:
                self.callbacks.buttons.clicked.south()

        if self.gamepadState.buttons.north == 0 and previous_north_button == 1: 
            if self.callbacks.buttons.clicked.north is not None:
                self.callbacks.buttons.clicked.north()

        if self.gamepadState.buttons.east == 0 and previous_east_button == 1: 
            if self.callbacks.buttons.clicked.east is not None:
                self.callbacks.buttons.clicked.east()

        if self.gamepadState.buttons.west == 0 and previous_west_button == 1: 
            if self.callbacks.buttons.clicked.west is not None:
                self.callbacks.buttons.clicked.west()

        ## Pressed (on hold down)
        if self.gamepadState.buttons.south == 1 and previous_south_button == 1: 
            if self.callbacks.buttons.pressed.south is not None:
                self.callbacks.buttons.pressed.south()
        
        if self.gamepadState.buttons.north == 1 and previous_north_button == 1: 
            if self.callbacks.buttons.pressed.north is not None:
                self.callbacks.buttons.pressed.north()

        if self.gamepadState.buttons.east == 1 and previous_east_button == 1: 
            if self.callbacks.buttons.pressed.east is not None:
                self.callbacks.buttons.pressed.east()
        
        if self.gamepadState.buttons.west == 1 and previous_west_button == 1: 
            if self.callbacks.buttons.pressed.west is not None:
                self.callbacks.buttons.pressed.west()

        # Triggers   
        if self.gamepadState.triggers.right.z != 0: 
            if self.callbacks.triggers.right.z is not None:
                self.callbacks.triggers.right.z(self.gamepadState.triggers.right.z)
            
        if self.gamepadState.triggers.left.z != 0: 
            if self.callbacks.triggers.left.z is not None:
                self.callbacks.triggers.left.z(self.gamepadState.triggers.left.z)

        if self.gamepadState.triggers.right.t != 0: 
            if self.callbacks.triggers.right.t is not None:
                self.callbacks.triggers.right.t(self.gamepadState.triggers.right.t)

        if self.gamepadState.triggers.left.t != 0: 
            if self.callbacks.triggers.left.t is not None:
                self.callbacks.triggers.left.t(self.gamepadState.triggers.left.t)
            
        # Joysticks
        if self.gamepadState.sticks.left.horizontal !=0 or self.gamepadState.sticks.left.vertical !=0: 
            if self.callbacks.sticks.left is not None:
                self.callbacks.sticks.left(self.gamepadState.sticks.left.horizontal, self.gamepadState.sticks.left.vertical)

        if self.gamepadState.sticks.right.horizontal !=0 or self.gamepadState.sticks.right.vertical !=0: 
            if self.callbacks.sticks.right is not None:
                self.callbacks.sticks.right(self.gamepadState.sticks.left.horizontal, self.gamepadState.sticks.right.vertical)
    