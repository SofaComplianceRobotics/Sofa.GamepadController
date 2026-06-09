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

    def __init__(self, callbacks: GamepadCallbacks = GamepadCallbacks(), index: int = 0, name: str = "GamepadController"):
        
        super().__init__()
        self.name = name
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

        previous_south_dpad = self.gamepadState.dpad.south
        previous_north_dpad = self.gamepadState.dpad.north
        previous_east_dpad = self.gamepadState.dpad.east
        previous_west_dpad = self.gamepadState.dpad.west

        previous_stick_left_button = self.gamepadState.sticks.left.button
        previous_stick_right_button = self.gamepadState.sticks.right.button

        for event in events_to_process:
            if event is None:
                continue
            
            # Update gamepad state based on the latest event
            self.gamepadState.update(event)
            
        # Based on the updated gamepad state, determine the target position and gripper state
        
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
            if self.callbacks.sticks.left.moved is not None:
                self.callbacks.sticks.left.moved(self.gamepadState.sticks.left.horizontal, self.gamepadState.sticks.left.vertical)

        if self.gamepadState.sticks.left.button == 1 and previous_stick_left_button == 1:
            if self.callbacks.sticks.left.pressed is not None:
                self.callbacks.sticks.left.pressed()

        if self.gamepadState.sticks.left.button == 0 and previous_stick_left_button == 1:
            if self.callbacks.sticks.left.released is not None:
                self.callbacks.sticks.left.released()

        if self.gamepadState.sticks.right.horizontal !=0 or self.gamepadState.sticks.right.vertical !=0: 
            if self.callbacks.sticks.right.moved is not None:
                self.callbacks.sticks.right.moved(self.gamepadState.sticks.right.horizontal, self.gamepadState.sticks.right.vertical)
    
        if self.gamepadState.sticks.right.button == 1 and previous_stick_right_button == 1:
            if self.callbacks.sticks.right.pressed is not None:
                self.callbacks.sticks.right.pressed()

        if self.gamepadState.sticks.right.button == 0 and previous_stick_right_button == 1:
            if self.callbacks.sticks.right.released is not None:
                self.callbacks.sticks.right.released()

        # Buttons
        ## Released 
        if self.gamepadState.buttons.south == 0 and previous_south_button == 1: 
            if self.callbacks.buttons.south.released is not None:
                self.callbacks.buttons.south.released()

        if self.gamepadState.buttons.north == 0 and previous_north_button == 1: 
            if self.callbacks.buttons.north.released is not None:
                self.callbacks.buttons.north.released()

        if self.gamepadState.buttons.east == 0 and previous_east_button == 1: 
            if self.callbacks.buttons.east.released is not None:
                self.callbacks.buttons.east.released()
        if self.gamepadState.buttons.west == 0 and previous_west_button == 1: 
            if self.callbacks.buttons.west.released is not None:
                self.callbacks.buttons.west.released()

        ## Pressed
        if self.gamepadState.buttons.south == 1 and previous_south_button == 1: 
            if self.callbacks.buttons.south.pressed is not None:
                self.callbacks.buttons.south.pressed()
        
        if self.gamepadState.buttons.north == 1 and previous_north_button == 1: 
            if self.callbacks.buttons.north.pressed is not None:
                self.callbacks.buttons.north.pressed()

        if self.gamepadState.buttons.east == 1 and previous_east_button == 1: 
            if self.callbacks.buttons.east.pressed is not None:
                self.callbacks.buttons.east.pressed()
        
        if self.gamepadState.buttons.west == 1 and previous_west_button == 1: 
            if self.callbacks.buttons.west.pressed is not None:
                self.callbacks.buttons.west.pressed()

        # D-pad
        ## Released
        if self.gamepadState.dpad.north == 0 and previous_north_dpad == 1:
            if self.callbacks.dpad.north.released is not None:
                self.callbacks.dpad.north.released()

        if self.gamepadState.dpad.south == 0 and previous_south_dpad == 1:
            if self.callbacks.dpad.south.released is not None:
                self.callbacks.dpad.south.released()

        if self.gamepadState.dpad.east == 0 and previous_east_dpad == 1:
            if self.callbacks.dpad.east.released is not None:
                self.callbacks.dpad.east.released()
        if self.gamepadState.dpad.west == 0 and previous_west_dpad == 1:
            if self.callbacks.dpad.west.released is not None:
                self.callbacks.dpad.west.released()

        ## Pressed
        if self.gamepadState.dpad.north == 1 and previous_north_dpad == 1:
            if self.callbacks.dpad.north.pressed is not None:
                self.callbacks.dpad.north.pressed()

        if self.gamepadState.dpad.south == 1 and previous_south_dpad == 1:
            if self.callbacks.dpad.south.pressed is not None:
                self.callbacks.dpad.south.pressed()
        if self.gamepadState.dpad.east == 1 and previous_east_dpad == 1:
            if self.callbacks.dpad.east.pressed is not None:
                self.callbacks.dpad.east.pressed()

        if self.gamepadState.dpad.west == 1 and previous_west_dpad == 1:
            if self.callbacks.dpad.west.pressed is not None:
                self.callbacks.dpad.west.pressed()