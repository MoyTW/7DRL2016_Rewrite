import json


class Config(object):
    def __init__(self, file_location):
        with open(file_location, 'r') as f:
            config = json.load(f)
            self.SCREEN_WIDTH = int(config["SCREEN_WIDTH"])
            self.SCREEN_HEIGHT = int(config["SCREEN_HEIGHT"])
            self.MAP_WIDTH = int(config["MAP_WIDTH"])
            self.MAP_HEIGHT = int(config["MAP_HEIGHT"])
            self.PANEL_HEIGHT = int(config["PANEL_HEIGHT"])
            self.FULL_SCREEN = bool(config["FULL_SCREEN"])
            self.CAMERA_WIDTH = int(config["CAMERA_WIDTH"])
            self.CAMERA_HEIGHT = int(config["CAMERA_HEIGHT"])
            self.VISION_RADIUS = int(config["VISION_RADIUS"])
            self.FOV_ALGO = int(config["FOV_ALGO"])
            self.FOV_LIGHT_WALLS = bool(config["FOV_LIGHT_WALLS"])
            # etc etc etc
