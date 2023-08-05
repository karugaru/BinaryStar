from enum import IntEnum
from math import hypot


class OrbitButtonType(IntEnum):
    CENTER = 0
    LEFT = 1
    TOPLEFT = 2
    TOP = 3
    TOPRIGHT = 4
    RIGHT = 5
    BOTTOMRIGHT = 6
    BOTTOM = 7
    BOTTOMLEFT = 8


class OrbitInput:
    def __init__(self):
        if type(self) is OrbitInput:
            raise Exception("OrbitInput must be subclassed.")


class OrbitJoyStickInput(OrbitInput):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def length(self) -> float:
        return hypot(self.x, self.y)


class OrbitButtonInput(OrbitInput):
    def __init__(self, button: OrbitButtonType, pressed: bool):
        self.button = button
        self.pressed = pressed


class OrbitRotateInput(OrbitInput):
    def __init__(self, clockwise: bool):
        self.clockwise = clockwise
