import time
from math import copysign

from orbit.config import read_settings
from orbit.control import (MOUSE_BUTTON_LEFT, MOUSE_BUTTON_MIDDLE,
                           MOUSE_BUTTON_RIGHT, mouse_move, mouse_scroll,
                           mouse_updown)
from orbit.orbitadapter import OrbitAdapter
from orbit.orbitinput import OrbitButtonType
from orbit.orbitstate import OrbitButtonEvent, OrbitRotateEvent, OrbitState

mouse_speed_scale = 4
scroll_clicks = 100
acceleration_dimension = 3

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
            mouse_scroll(scroll_clicks * (-1 if event.clockwise else 1))
        if isinstance(event, OrbitButtonEvent):
            if event.bystick:
                continue
            if event.button == OrbitButtonType.LEFT:
                mouse_updown(MOUSE_BUTTON_LEFT, not event.pressed)
            elif event.button == OrbitButtonType. RIGHT:
                mouse_updown(MOUSE_BUTTON_RIGHT, not event.pressed)
            elif event.button == OrbitButtonType.CENTER:
                mouse_updown(MOUSE_BUTTON_MIDDLE, not event.pressed)

    if state.length > state.setting.deadzone:
        x = copysign(state.x ** acceleration_dimension *
                     mouse_speed_scale, state.x)
        y = copysign(state.y ** acceleration_dimension *
                     mouse_speed_scale, -state.y)
        mouse_move(x, y)
