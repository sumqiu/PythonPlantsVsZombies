"""
Map loading and background setup
"""
import json
from pathlib import Path
import pygame as pg
from ... import tool
from ... import constants as c

# source/state/level/ -> source/state/ -> source/
_SOURCE_DIR = Path(__file__).parent.parent.parent


class MapLoader:
    def __init__(self, level):
        self.level = level
    
    def loadMap(self):
        """Load map data from JSON file"""
        map_file = f"level_{self.level.game_info[c.LEVEL_NUM]}.json"
        file_path = _SOURCE_DIR / 'data' / 'map' / map_file
        with open(file_path) as f:
            self.level.map_data = json.load(f)
    
    def setupBackground(self):
        """Setup background image and viewport"""
        img_index = self.level.map_data[c.BACKGROUND_TYPE]
        self.level.background_type = img_index
        self.level.background = tool.GFX[c.BACKGROUND_NAME][img_index]
        self.level.bg_rect = self.level.background.get_rect()

        self.level.level = pg.Surface((self.level.bg_rect.w, self.level.bg_rect.h)).convert()
        self.level.viewport = tool.SCREEN.get_rect(bottom=self.level.bg_rect.bottom)
        self.level.viewport.x += c.BACKGROUND_OFFSET_X
