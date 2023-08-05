from collections import deque
from math import atan2, degrees, hypot

from orbit.config import Setting
from orbit.orbitinput import (OrbitButtonInput, OrbitButtonType, OrbitInput,
                              OrbitJoyStickInput, OrbitRotateInput)


class OrbitEvent:
    def __init__(self):
        if type(self) is OrbitEvent:
            raise Exception("OrbitEvent must be subclassed.")


class OrbitJoyStickEvent(OrbitEvent):
    def __init__(self, x: float, y: float, dx: float, dy: float):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def __str__(self) -> str:
        return f'joystick: x={self.x} y={self.y} dx={self.x} dy={self.y}'


class OrbitRotateEvent(OrbitEvent):
    def __init__(self, clockwise: bool):
        self.clockwise = clockwise

    def __str__(self) -> str:
        return f'''rotate: {'cw' if self.clockwise else 'ccw'}'''


class OrbitButtonEvent(OrbitEvent):
    def __init__(self, button: OrbitButtonType, pressed: bool, bystick: bool):
        self.button = button
        self.pressed = pressed
        self.bystick = bystick

    def __str__(self) -> str:
        return f'button: id={self.button} pressed={self.pressed} bystick={self.bystick}'


class OrbitState:
    def __init__(self, setting: Setting) -> None:
        self.setting = setting
        self.x = 0.0
        self.y = 0.0
        self.button = [False, False, False, False,
                       False, False, False, False, False]
        self.__bystick = [False, False, False, False,
                          False, False, False, False, False]
        self.__events: deque[OrbitEvent] = deque()

    @property
    def length(self) -> float:
        return hypot(self.x, self.y)

    def __str__(self) -> str:
        return (
            f'x={self.x}'
            + f' y={self.y}'
            + f' length={self.length}'
            + f' button={self.button}'
        )

    def pop_event(self) -> OrbitEvent | None:
        if len(self.__events) <= 0:
            return None
        else:
            return self.__events.popleft()

    def apply_input(self, orbit_input: OrbitInput):
        if isinstance(orbit_input, OrbitJoyStickInput):
            x = float(orbit_input.x - self.setting.center_x)
            if x > 0:
                x = x / self.setting.max_x
            else:
                x = x / abs(self.setting.min_x)
            y = float(orbit_input.y - self.setting.center_y)
            if y > 0:
                y = y / self.setting.max_y
            else:
                y = y / abs(self.setting.min_y)
            if hypot(x, y) > self.setting.deadzone:
                self.__events.append(
                    OrbitJoyStickEvent(x, y, x - self.x, y - self.y))
            self.x = x
            self.y = y
        elif isinstance(orbit_input, OrbitRotateInput):
            self.__events.append(OrbitRotateEvent(orbit_input.clockwise))
        elif isinstance(orbit_input, OrbitButtonInput):
            # ジョイスティックボタン操作
            if orbit_input.pressed and orbit_input.button == OrbitButtonType.CENTER:
                if self.button[OrbitButtonType.CENTER] != orbit_input.pressed:
                    self.__events.append(
                        OrbitButtonEvent(
                            OrbitButtonType.CENTER,
                            orbit_input.pressed,
                            False))
                self.button[OrbitButtonType.CENTER] = orbit_input.pressed
            # ジョイスティックを動かして押すボタン操作
            elif self.length > self.setting.presszone and orbit_input.pressed:
                # deg -> left:0° top:90° right:180° bottom:270°
                deg = degrees(atan2(-self.y, self.x)) + 180
                # 1つのスイッチの領域が360°/8あるので、スイッチが領域の中心になるように
                # 360°/16だけ領域をずらす
                deg = (deg + 360 / 16) % 360
                button = int(deg / (360 / 8)) + 1
                if self.button[button] is not True:
                    self.__events.append(
                        OrbitButtonEvent(
                            OrbitButtonType(button),
                            True,
                            True))
                for i in range(1, 9):
                    self.button[i] = False
                    self.__bystick[i] = False
                self.button[button] = True
                self.__bystick[button] = True
            # 上記以外のボタン押下操作
            elif orbit_input.pressed:
                # orbitalはボタン離上操作を報告しないことがあるので、
                # ボタンが押下された=押下されているボタンは離上された
                # としてソフト側で認識する必要がある
                for i in range(1, 9):
                    if self.button[i]:
                        self.__events.append(
                            OrbitButtonEvent(
                                OrbitButtonType(i),
                                False,
                                self.__bystick[i]))
                    self.button[i] = False
                    self.__bystick[i] = False
                self.button[orbit_input.button] = True
                self.__events.append(
                    OrbitButtonEvent(
                        OrbitButtonType(orbit_input.button),
                        True,
                        False))
            # 上記以外のボタン離上操作
            else:
                # orbitalはボタン離上操作を1操作につき複数回報告することがあるので、
                # ボタンが押下されていて、かつ離上された場合にのみイベントキューを積む必要がある
                if self.button[orbit_input.button]:
                    self.__events.append(
                        OrbitButtonEvent(
                            OrbitButtonType(orbit_input.button),
                            False,
                            self.__bystick[orbit_input.button]))
                self.button[orbit_input.button] = False
                self.__bystick[orbit_input.button] = False
