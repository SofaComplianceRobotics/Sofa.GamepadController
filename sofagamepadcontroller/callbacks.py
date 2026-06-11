from typing import Callable


class _Stick:
    """Class to hold the callbacks for a stick.

    Parameters:
        moved: Callable[[int, int], None] = None
            Callback for stick movement, takes horizontal and vertical values as input
        released: Callable[[None], None] = None
            Callback for stick release, takes the stick value as input
        pressed: Callable[[None], None] = None
            Callback for stick press, takes the stick value as input
    """
    def __init__(self):
        self.moved: Callable[[int, int], None] = None
        self.released: Callable[[None], None] = None
        self.pressed: Callable[[None], None] = None


class _Sticks:
    """Class to hold the callbacks for the sticks.

    Parameters:
        left: _Stick = _Stick()
            Callbacks for the left stick
        right: _Stick = Stick()
            Callbacks for the right stick
    """
    def __init__(self):
        self.left: _Stick = _Stick()
        self.right: _Stick = _Stick()


class _Trigger:
    """Class to hold the callbacks for a trigger.

    Parameters:
        t: Callable[[int], None] = None
            Callback for the trigger, takes the trigger value as input
        z: Callable[[int], None] = None
            Callback for the trigger, takes the trigger value as input
    """
    def __init__(self):
        self.t: Callable[[int], None] = None
        self.z: Callable[[int], None] = None


class _Triggers:
    """Class to hold the callbacks for the triggers.

    Parameters:
        left: _Trigger = _Trigger()
            Left trigger callbacks
        right: _Trigger = _Trigger()
            Right trigger callbacks
    """
    def __init__(self):
        self.left: _Trigger = _Trigger()
        self.right: _Trigger = _Trigger()


class _Button:
    """Class to hold the callbacks for the buttons.

    Parameters:
        released: Callable[[None], None] = None
            Callback for button release
        pressed: Callable[[None], None] = None
            Callback for button press
    """
    def __init__(self):
        self.released: Callable[[None], None] = None
        self.pressed: Callable[[None], None] = None


class _Directional:
    """Class to hold the callbacks for the directional inputs.

    Parameters:
        south: _Button = _Button()
            South button callbacks
        north: _Button = _Button()
            North button callbacks
        east: _Button = _Button()
            East button callbacks
        west: _Button = _Button()
            West button callbacks
    """
    def __init__(self):
        self.south: _Button = _Button()
        self.north: _Button = _Button()
        self.east: _Button = _Button()
        self.west: _Button = _Button()


class GamepadCallbacks:
    """Class to hold the callbacks for the different gamepad inputs.

    Parameters:
        sticks: _Sticks = _Sticks()
            Callbacks for the sticks
        triggers: _Triggers = _Triggers()
            Callbacks for the triggers
        buttons: _Directional = _Directional()
            Callbacks for the buttons
        dpad: _Directional = _Directional()
            Callbacks for the d-pad
    """
    def __init__(self):
        self.sticks: _Sticks = _Sticks()
        self.triggers: _Triggers = _Triggers()
        self.buttons: _Directional = _Directional()
        self.dpad: _Directional = _Directional()
