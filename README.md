# Sofa.GamepadController
This module allows you to handle gamepad events in your SOFA scene.

<img src="images/xbox_controller_mappings.jpg" width="800px"></img>

## Requirements

SOFA with the SofaPython3 plugin, and the `inputs` Python library. You can install it with pip:

`python3 -m pip install inputs`

## Usage

There are two important classes for users: `GamepadSofaController` and `GamepadCallbacks`

`GamepadSofaController` needs to be fed a `GamepadCallbacks` object that implements callbacks for the events that you are interested into.

For example, if you just want to react to a released `A` button or a left stick movement:

```python
from gamepad import GamepadSofaController, GamepadCallbacks

def createScene(rootnode):

    def printAReleased():
        print("You released A button!")

    def printLeftStickMoved(horizontal, vertical):
        print(f"Left stick moved: horizontal={horizontal}, vertical={vertical}")

    callbacks = GamepadCallbacks()
    callbacks.buttons.south.released = printAReleased
    callbacks.sticks.left.moved = printLeftStickMoved
    # Adds the controller to thhe SOFA scene
    rootnode.addObject(GamepadSofaController(callbacks=callbacks))
```

You can also run the example scene in [`runSofa -lSofaPython3 example.py`](example.py) to see how to use the module. It moves a frame in the scene using the left and right sticks. You can also click the `A` button to invert the axis of the sticks.

**Important**: The callbacks have a typed signature, check the docstring. You can use captured variables to modify objects inside the callback.

**Note**: On Windows, if you want to use Dualshock 4 controllers, install [DS4Windows](https://ds4-windows.com/get-started/). This emulates XBox controllers and make the gamepad compatible with Windows 10+.

### List of callbacks

**Buttons:**
- `callbacks.buttons.north.pressed()`
- `callbacks.buttons.north.released()`
- `callbacks.buttons.south.pressed()`
- `callbacks.buttons.south.released()`
- `callbacks.buttons.east.pressed()`
- `callbacks.buttons.east.released()`
- `callbacks.buttons.west.pressed()`
- `callbacks.buttons.west.released()`

**Dpad:**
- `callbacks.dpad.north.pressed()`
- `callbacks.dpad.north.released()`
- `callbacks.dpad.south.pressed()`
- `callbacks.dpad.south.released()`
- `callbacks.dpad.east.pressed()`
- `callbacks.dpad.east.released()`
- `callbacks.dpad.west.pressed()`
- `callbacks.dpad.west.released()`

**Sticks:**
- `callbacks.sticks.left.moved(horizontal: float, vertical: float)`
- `callbacks.sticks.left.pressed()`
- `callbacks.sticks.left.released()`
- `callbacks.sticks.right.moved(horizontal: float, vertical: float)`
- `callbacks.sticks.right.pressed()`
- `callbacks.sticks.right.released()`

**Triggers:**
- `callbacks.triggers.left.t()`
- `callbacks.triggers.left.z(value: float)`
- `callbacks.triggers.right.t()`
- `callbacks.triggers.right.z(value: float)`

## Supported Controllers

The following controllers have been tested and are supported by the module:

- Official Microsoft XBox Series
- TurtleBeach Rematch for XBox (Windows only)
- Official Sony Dualshock 4

In the file `state.py` you can find the mapping of the buttons and axes for each controller. If you want to add support for a new controller, you can add the mapping in that file and submit a PR. The sticks are mapped between -1 and 1, and the triggers are mapped between 0 and 1.