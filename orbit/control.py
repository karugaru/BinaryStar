import pyautogui

pyautogui.PAUSE = 0

__x_acc = 0.0
__y_acc = 0.0

MOUSE_BUTTON_LEFT = 'left'
MOUSE_BUTTON_RIGHT = 'right'
MOUSE_BUTTON_MIDDLE = 'middle'


def mouse_move(x: float, y: float):
    global __x_acc
    global __y_acc
    __x_acc += x
    __y_acc += y
    pyautogui.moveRel(int(__x_acc), int(__y_acc))
    __x_acc -= int(__x_acc)
    __y_acc -= int(__y_acc)


def mouse_scroll(clicks: int):
    pyautogui.scroll(clicks)


def mouse_down(button: str):
    pyautogui.mouseDown(button=button)


def mouse_up(button: str):
    pyautogui.mouseUp(button=button)


def mouse_updown(button: str, up: bool):
    if up:
        mouse_up(button)
    else:
        mouse_down(button)


def key_down(key: str):
    pyautogui.keyDown(key)


def key_up(key: str):
    pyautogui.keyUp(key)


def key_press(key: str):
    pyautogui.press(key)


def key_updown(key: str, up: bool):
    if up:
        key_up(key)
    else:
        key_down(key)
