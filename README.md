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
    callbacks.buttons.released.south = printAReleased
    callbacks.sticks.left = printLeftStickMoved
    # Adds the controller to thhe SOFA scene
    rootnode.addObject(GamepadSofaController(callbacks=callbacks))
```

You can also run the example scene in [`runSofa -lSofaPython3 example.py`](example.py) to see how to use the module. It moves a frame in the scene using the left and right sticks. You can also click the `A` button to invert the axis of the sticks.

**Important**: The callbacks have a typed signature, check the docstring. You can use captured variables to modify objects inside the callback.

**Note**: On Windows, if you want to use Dualshock 4 controllers, install [DS4Windows](https://ds4-windows.com/get-started/). This emulates XBox controllers and make the gamepad compatible with Windows 10+.

## Supported Controllers

The following controllers have been tested and are supported by the module:

- Official Microsoft XBox Series
- TurtleBeach Rematch for XBox (Windows only)
- Official Sony Dualshock 4

In the file `state.py` you can find the mapping of the buttons and axes for each controller. If you want to add support for a new controller, you can add the mapping in that file and submit a PR. The sticks are mapped between -1 and 1, and the triggers are mapped between 0 and 1.