from enum import Enum


class _Directional:
    def __init__(self):    
        self.vertical: int = 0
        self.horizontal: int = 0
        self.button: int = 0

class _Trigger():
    def __init__(self):
        self.t: int = 0
        self.z: int = 0

class _Sticks():
    def __init__(self):
        self.left: _Directional = _Directional()
        self.right: _Directional = _Directional()

class _Triggers:
    def __init__(self):
        self.left: _Trigger = _Trigger()
        self.right: _Trigger = _Trigger()

class _Buttons:
    def __init__(self):
        self.south: int = 0
        self.north: int = 0
        self.east: int = 0
        self.west: int = 0

class GamepadState:
    def __init__(self):
        self.sticks: _Sticks = _Sticks()
        self.triggers: _Triggers = _Triggers()
        self.buttons: _Buttons = _Buttons()
        self.dpad: _Buttons = _Buttons()

    def update(self, event):
        """Update the gamepad state based on the latest event.
        This method will be overridden by specific gamepad classes (e.g., XBox, Sony) to handle their unique event codes.
        """
        if event.code == "BTN_SOUTH": 
            self.buttons.south = event.state
        elif event.code == "BTN_NORTH":
            self.buttons.north = event.state
        elif event.code == "BTN_EAST":
            self.buttons.east = event.state
        elif event.code == "BTN_WEST":
            self.buttons.west = event.state
        elif event.code == "ABS_HAT0X": 
            self.dpad.east = 1 if event.state == 1 else 0
            self.dpad.west = 1 if event.state == -1 else 0
        elif event.code == "ABS_HAT0Y": 
            self.dpad.north = 1 if event.state == -1 else 0
            self.dpad.south = 1 if event.state == 1 else 0
        elif event.code == "BTN_THUMBL": 
            self.sticks.left.button = event.state
        elif event.code == "BTN_THUMBR":
            self.sticks.right.button = event.state
        elif event.code == "BTN_TL":     
            self.triggers.left.t = event.state
        elif event.code == "BTN_TR":     
            self.triggers.right.t = event.state

class XBoxTurtleBeach(GamepadState):

    def get_name(self):
        return "XBoxTurtleBeach"

    def update(self, event):
        """Update the gamepad state based on the latest event.
        - sticks values range from -32768 to 32767, with 0 being the centered position
        - triggers values range from 0 to 255, with 0 being not pressed and 255 being fully pressed
        """
        super().update(event) # Update button states using the base class method

        # Normalize all values to be between -1 and 1
        if event.code == "ABS_X":
            self.sticks.left.horizontal = event.state / 32768
        elif event.code == "ABS_Y":
            self.sticks.left.vertical = event.state / 32768 
        elif event.code == "ABS_RX":
            self.sticks.right.horizontal = event.state / 32768
        elif event.code == "ABS_RY":
            self.sticks.right.vertical = event.state / 32768 
        elif event.code == "ABS_Z":
            self.triggers.left.z = event.state / 255 
        elif event.code == "ABS_RZ":
            self.triggers.right.z = event.state / 255 
        

class XBox(GamepadState):

    def get_name(self):
        return "XBox"

    def update(self, event):
        """Update the gamepad state based on the latest event.
        - sticks values range from -32768 to 32767, with 0 being the centered position
        - triggers values range from 0 to 1024, with 0 being not pressed and 1024 being fully pressed
        """
        super().update(event) # Update button states using the base class method

        # Normalize all values to be between -1 and 1
        if event.code == "ABS_X":
            self.sticks.left.horizontal = event.state / 32768 if not -2000 <= event.state <= 2000 else 0 # Deadzone around the centered position to avoid drift
        elif event.code == "ABS_Y":
            self.sticks.left.vertical = event.state / 32768 if not -2000 <= event.state <= 2000 else 0 
        elif event.code == "ABS_RX":
            self.sticks.right.horizontal = event.state / 32768 if not -2000 <= event.state <= 2000 else 0
        elif event.code == "ABS_RY":
            self.sticks.right.vertical = event.state / 32768 if not -2000 <= event.state <= 2000 else 0
        elif event.code == "ABS_Z":
            self.triggers.left.z = event.state / 1024 
        elif event.code == "ABS_RZ":
            self.triggers.right.z = event.state / 1024 


class Sony(GamepadState):

    def get_name(self):
        return "Sony"
    
    def update(self, event):
        """Update the gamepad state based on the latest event.
        - sticks values range from 0 to 255, with 128 being the centered position
        - triggers values range from 0 to 255, with 0 being not pressed and 255 being fully pressed
        """
        super().update(event) # Update button states using the base class method

        # Normalize all values to be between -1 and 1
        if event.code == "ABS_X":
            self.sticks.left.horizontal = (event.state - 128) / 127 if not 118 <= event.state <= 138 else 0 # Deadzone of 10% around the centered position to avoid drift
        elif event.code == "ABS_Y":
            self.sticks.left.vertical = - (event.state - 128) / 127 if not 118 <= event.state <= 138 else 0 
        elif event.code == "ABS_RX":
            self.sticks.right.horizontal = (event.state - 128) / 127 if not 118 <= event.state <= 138 else 0
        elif event.code == "ABS_RY":
            self.sticks.right.vertical = - (event.state - 128) / 127 if not 118 <= event.state <= 138 else 0
        elif event.code == "ABS_Z":
            self.triggers.left.z = event.state / 255 
        elif event.code == "ABS_RZ":
            self.triggers.right.z = event.state / 255 


class GamepadType(Enum):
    XBOX = "microsoftxbox"
    XBOX_TURTLE_BEACH = "xbox"
    SONY = "sony"

    def get_gamepad_class(gamepad_name):
        import re
        pattern = r'[\W_]' 
        alphanum = re.sub(pattern,"", gamepad_name.lower()) # strip from non alpha-numeric characters

        if  GamepadType.XBOX.value in alphanum:
            return XBox
        elif  GamepadType.XBOX_TURTLE_BEACH.value in alphanum:
            return XBoxTurtleBeach
        elif  GamepadType.SONY.value in alphanum:
            return Sony
        else:
            raise ValueError("Unsupported gamepad type")