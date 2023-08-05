import time

import keyboard

from orbit.config import read_settings, write_settings
from orbit.orbitadapter import OrbitAdapter
from orbit.orbitinput import OrbitJoyStickInput

mouse_speed_scale = 1.5

setting = read_settings()
orbit = OrbitAdapter()
time.sleep(0.1)
print('connected')

max_x = 0
max_y = 0
min_x = 0
min_y = 0
print('Move the joystick to the maximum in all directions')
print('Press enter when finished')
while True:
    time.sleep(0.0001)
    if keyboard.is_pressed("enter"):
        input()
        break

    if orbit.readable():
        orbit_input = orbit.read_input()
        if orbit_input is not None and isinstance(orbit_input, OrbitJoyStickInput):
            max_x = max(max_x, orbit_input.x)
            max_y = max(max_y, orbit_input.y)
            min_x = min(min_x, orbit_input.x)
            min_y = min(min_y, orbit_input.y)
print(f'max_x:{max_x} max_y:{max_y} min_x:{min_x} min_y:{min_y}')

while True:
    time.sleep(0.0001)
    if not keyboard.is_pressed("enter"):
        break

center_x = 0
center_y = 0
print('Move the joystick back to the center')
print('Press enter when finished')
while True:
    time.sleep(0.0001)
    if keyboard.is_pressed("enter"):
        input()
        break

    if orbit.readable():
        orbit_input = orbit.read_input()
        if orbit_input is not None and isinstance(orbit_input, OrbitJoyStickInput):
            center_x = orbit_input.x
            center_y = orbit_input.y
print(f'center_x:{center_x} center_y:{center_y}')

setting.max_x = max_x
setting.max_y = max_y
setting.min_x = min_x
setting.min_y = min_y
setting.center_x = center_x
setting.center_y = center_y
write_settings(setting)

print('Settings is saved')
