import json
from os.path import isfile

__SETTING_FILE_PATH = 'settings.json'


class Setting():
    def __init__(self, center_x: int = 0, center_y: int = 0,
                 max_x: int = 80, max_y: int = 80,
                 min_x: int = -80, min_y: int = -80,
                 deadzone: float = 0.1, presszone: float = 0.9):
        self.center_x = center_x
        self.center_y = center_y
        self.max_x = max_x
        self.max_y = max_y
        self.min_x = min_x
        self.min_y = min_y
        self.deadzone = deadzone
        self.presszone = presszone


def read_settings():
    if isfile(__SETTING_FILE_PATH):
        with open(__SETTING_FILE_PATH, 'r') as json_file:
            json_data = json.load(json_file)
            center_x = json_data['center_x']
            center_y = json_data['center_y']
            max_x = json_data['max_x']
            max_y = json_data['max_y']
            min_x = json_data['min_x']
            min_y = json_data['min_y']
            deadzone = json_data['deadzone']
            presszone = json_data['presszone']
            return Setting(center_x, center_y,
                           max_x, max_y,
                           min_x, min_y,
                           deadzone, presszone)
    return Setting()


def write_settings(setting: Setting):
    with open(__SETTING_FILE_PATH, 'w') as json_file:
        json.dump({
            'center_x': setting.center_x,
            'center_y': setting.center_y,
            'max_x': setting.max_x,
            'max_y': setting.max_y,
            'min_x': setting.min_x,
            'min_y': setting.min_y,
            'deadzone': setting.deadzone,
            'presszone': setting.presszone,
        }, json_file, indent=2)
