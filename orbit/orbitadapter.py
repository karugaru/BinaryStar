import serial
import serial.tools.list_ports

from orbit.orbitinput import (OrbitButtonInput, OrbitButtonType, OrbitInput,
                              OrbitJoyStickInput, OrbitRotateInput)


def _read_and_test(serial: serial.Serial, size: int, expected: str) -> bool:
    bytes = serial.read(size)
    if len(bytes) != size:
        return False
    return str(bytes, encoding='ascii') == expected


def _convert_xy(x: bytes, y: bytes):
    if len(x) != 1 or len(y) != 1:
        return None
    return (x[0] - 128, y[0] - 128)


class OrbitAdapter:
    def __init__(self) -> None:
        ports = serial.tools.list_ports.comports()
        availablePorts = list(filter(lambda x: x.vid == 0x3525, ports))
        if len(availablePorts) == 0:
            raise RuntimeError('Cound not found Orbital device.')
        self.serial = serial.Serial(
            availablePorts[0].device, 115200, timeout=0.05)

    def readable(self):
        return self.serial.in_waiting > 0

    def close(self):
        self.serial.close()

    def read_input(self) -> OrbitInput | None:  # noqa: max-complexity
        if not self.readable():
            return None
        bytes = self.serial.read(1)
        if len(bytes) == 0:
            return None

        if bytes[0] == ord('J'):
            if not _read_and_test(self.serial, 2, 'SX'):
                return None
            x = self.serial.read(1)
            if not _read_and_test(self.serial, 1, 'Y'):
                return None
            y = self.serial.read(1)
            if not _read_and_test(self.serial, 1, ';'):
                return None
            xy = _convert_xy(x, y)
            if xy is None:
                return None
            return OrbitJoyStickInput(xy[0], xy[1])

        elif bytes[0] == ord('R'):
            typeBytes = self.serial.read(1)
            if len(typeBytes) != 1:
                return None
            if typeBytes[0] == ord('E'):
                if not _read_and_test(self.serial, 1, '-'):
                    return None
                directionBytes = self.serial.read(1)
                if len(directionBytes) != 1:
                    return None
                clockwise = directionBytes[0] == ord('R')
                if not _read_and_test(self.serial, 1, ';'):
                    return None
                return OrbitRotateInput(clockwise)

            elif typeBytes[0] == ord('C'):
                if not _read_and_test(self.serial, 2, '4='):
                    return None
                pressedBytes = self.serial.read(1)
                if len(pressedBytes) != 1:
                    return None
                pressed = pressedBytes[0] == ord('1')
                if not _read_and_test(self.serial, 1, ';'):
                    return None
                return OrbitButtonInput(OrbitButtonType.CENTER, pressed)

        elif bytes[0] == ord('S'):
            if not _read_and_test(self.serial, 1, 'W'):
                return None
            directionBytes = self.serial.read(1)
            if len(directionBytes) != 1:
                return None
            direction = directionBytes[0] - ord('0')
            if not _read_and_test(self.serial, 1, '='):
                return None
            pressedBytes = self.serial.read(1)
            if len(pressedBytes) != 1:
                return None
            pressed = pressedBytes[0] == ord('1')
            if not _read_and_test(self.serial, 1, ';'):
                return None
            return OrbitButtonInput(OrbitButtonType(direction), pressed)
        return None
