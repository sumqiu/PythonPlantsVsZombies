"""
Main Level class - coordinates all level components
"""
__author__ = 'marble_xu'

import pygame as pg
from ... import tool
from ... import constants as c
from ...component import map
from ...component.pause_menu import PauseMenu

from .map_loader import MapLoader
from .entity_manager import EntityManager
from .collision_handler import CollisionHandler
from .game_state_checker import GameStateChecker
from .renderer import LevelRenderer
from .input_handler import InputHandler


class Level(tool.State):
    def __init__(self):
        tool.State.__init__(self)
    
    def startup(self, current_time, persist):
        self.game_info = persist
        self.persist = self.game_info
        self.game_info[c.CURRENT_TIME] = current_time
        self.map_y_len = c.GRID_Y_LEN
        self.map = map.Map(c.GRID_X_LEN, self.map_y_len)
        
        # Initialize sub-modules
        self.map_loader = MapLoader(self)
        self.entity_manager = EntityManager(self)
        self.collision_handler = CollisionHandler(self)
        self.game_state_checker = GameStateChecker(self)
        self.renderer = LevelRenderer(self)
        self.input_handler = InputHandler(self)
        
        # Initialize pause menu
        self.pause_menu = PauseMenu()
        self.paused = False
        
        self.map_loader.loadMap()
        self.map_loader.setupBackground()
        self.initState()
        
        # Play level music based on background type
        if self.background_type == c.BACKGROUND_DAY:
            tool.music_manager.play_music(c.MUSIC_LEVEL_DAY)
        elif self.background_type == c.BACKGROUND_NIGHT:
            tool.music_manager.play_music(c.MUSIC_LEVEL_NIGHT)

    def initState(self):
        if c.CHOOSEBAR_TYPE in self.map_data:
            self.bar_type = self.map_data[c.CHOOSEBAR_TYPE]
        else:
            self.bar_type = c.CHOOSEBAR_STATIC

        if self.bar_type == c.CHOOSEBAR_STATIC:
            self.input_handler.initChoose()
        else:
            from ...component import menubar
            card_pool = menubar.getCardPool(self.map_data[c.CARD_POOL])
            self.input_handler.initPlay(card_pool)
            if self.bar_type == c.CHOOSEBAR_BOWLING:
                self.entity_manager.initBowlingMap()

    def update(self, surface, current_time, mouse_pos, mouse_click):
        self.current_time = self.game_info[c.CURRENT_TIME] = current_time
        
        if self.state == c.CHOOSE:
            self.input_handler.choose(mouse_pos, mouse_click)
        elif self.state == c.PLAY:
            if self.paused:
                self.input_handler.handlePause(mouse_pos, mouse_click)
            else:
                self.input_handler.play(mouse_pos, mouse_click)
        
        self.draw(surface)

    def draw(self, surface):
        self.renderer.draw(surface)
