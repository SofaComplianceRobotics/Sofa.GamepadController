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


class _Sticks:
    """Class to hold the callbacks for the sticks.
    
    Parameters:
        left: Callable[[int, int], None] = None 
            Callback for the left stick, takes horizontal and vertical values as input
        right: Callable[[int, int], None] = None
            Callback for the right stick, takes horizontal and vertical values as input
    """
    left: Callable[[int, int], None] = None
    right: Callable[[int, int], None] = None
    

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
        clicked: _Directional = _Directional()
            Callbacks for button click events (on release) in each direction
        pressed: _Directional = _Directional()
            Callbacks for button press events (on hold down) in each direction
    """
    clicked : _Directional = _Directional()
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
