import time

from orbit.config import read_settings
from orbit.control import (key_press, key_updown)
from orbit.orbitadapter import OrbitAdapter
from orbit.orbitinput import OrbitButtonType
from orbit.orbitstate import OrbitButtonEvent, OrbitRotateEvent, OrbitState

setting = read_settings()
orbit = OrbitAdapter()
time.sleep(0.1)
print('connected')

state = OrbitState(setting)

while True:
    time.sleep(0.0001)
    if orbit.readable():
        orbit_input = orbit.read_input()
        if orbit_input is not None:
            state.apply_input(orbit_input)

    while True:
        event = state.pop_event()
        if event is None:
            break
        if isinstance(event, OrbitRotateEvent):
            if event.clockwise:
                key_press('right')
            else:
                key_press('left')

        if isinstance(event, OrbitButtonEvent):
            match event.button:
                case OrbitButtonType.CENTER:
                    key_updown('playpause', not event.pressed)
                case OrbitButtonType.LEFT:
                    key_updown('prevtrack', not event.pressed)
                case OrbitButtonType.TOPLEFT:
                    pass
                case OrbitButtonType.TOP:
                    key_updown('up', not event.pressed)
                case OrbitButtonType.TOPRIGHT:
                    pass
                case OrbitButtonType.RIGHT:
                    key_updown('nexttrack', not event.pressed)
                case OrbitButtonType.BOTTOMRIGHT:
                    pass
                case OrbitButtonType.BOTTOM:
                    key_updown('down', not event.pressed)
                case OrbitButtonType.BOTTOMLEFT:
                    pass
