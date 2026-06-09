from typing import Callable


class _Trigger:
    """Class to hold the callbacks for a trigger.
    
    Parameters:
        t: Callable[[int], None] = None
            Callback for the trigger, takes the trigger value as input
        z: Callable[[int], None] = None
            Callback for the trigger, takes the trigger value as input
    """
    t: Callable[[int], None] = None
    z: Callable[[int], None] = None


class _Directional:
    """Class to hold the callbacks for the directional inputs.
    
    Parameters:
        south: Callable[[int], None] = None
            Callback for the south direction, takes the direction value as input
        north: Callable[[int], None] = None
            Callback for the north direction, takes the direction value as input
        east: Callable[[int], None] = None
            Callback for the east direction, takes the direction value as input
        west: Callable[[int], None] = None
            Callback for the west direction, takes the direction value as input
    """
    south: Callable[[int], None] = None
    north: Callable[[int], None] = None
    east: Callable[[int], None] = None
    west: Callable[[int], None] = None


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
    moved: Callable[[int, int], None] = None
    released: Callable[[None], None] = None
    pressed: Callable[[None], None] = None


class _Sticks:
    """Class to hold the callbacks for the sticks.
    
    Parameters:
        left: _Stick = _Stick()
            Callbacks for the left stick
        right: _Stick = Stick()
            Callbacks for the right stick
    """
    left: _Stick = _Stick()
    right: _Stick = _Stick()


class _Triggers:
    """Class to hold the callbacks for the triggers.
    
    Parameters:
        left: _Trigger = _Trigger()
            Left trigger callbacks
        right: _Trigger = _Trigger()
            Right trigger callbacks
    """
    left: _Trigger = _Trigger()
    right: _Trigger = _Trigger()


class _Buttons:
    """Class to hold the callbacks for the buttons.

    Parameters:
        released: _Directional = _Directional()
            Callbacks for button click events (on release) in each direction
        pressed: _Directional = _Directional()
            Callbacks for button press events (on hold down) in each direction
    """
    released : _Directional = _Directional()
    pressed : _Directional = _Directional()


class GamepadCallbacks:
    """Class to hold the callbacks for the different gamepad inputs.
    
    Parameters:
        sticks: _Sticks = _Sticks()
            Callbacks for the sticks
        triggers: _Triggers = _Triggers()
            Callbacks for the triggers
        buttons: _Buttons = _Buttons()
            Callbacks for the buttons
    """

    sticks : _Sticks = _Sticks()
    triggers : _Triggers = _Triggers()
    buttons : _Buttons = _Buttons()
    dpad : _Buttons = _Buttons()
