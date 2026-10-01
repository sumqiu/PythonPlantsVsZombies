__author__ = 'marble_xu'

import pygame as pg
from .. import tool
from .. import constants as c

class Screen(tool.State):
    def __init__(self):
        tool.State.__init__(self)
        self.end_time = 3000

    def startup(self, current_time, persist):
        self.start_time = current_time
        self.next = c.LEVEL
        self.persist = persist
        self.game_info = persist
        name = self.getImageName()
        self.setupImage(name)
        self.next = self.set_next_state()
        
        # Play screen music
        self.playMusic()
    
    def getImageName(self):
        pass

    def set_next_state(self):
        pass
    
    def playMusic(self):
        """Override in subclasses to play specific music."""
        pass

    def setupImage(self, name):
        frame_rect = [0, 0, 800, 600]
        self.image = tool.get_image(tool.GFX[name], *frame_rect)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, surface, current_time, mouse_pos, mouse_click):
        if(current_time - self.start_time) < self.end_time:
            surface.fill(c.WHITE)
            surface.blit(self.image, self.rect)
        else:
            self.done = True

class GameVictoryScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
    
    def getImageName(self):
        return c.GAME_VICTORY_IMAGE
    
    def set_next_state(self):
        # 如果是从关卡选择进入的，返回关卡选择界面
        if self.game_info.get('from_level_select', False):
            return c.LEVEL_SELECT
        # 已经打穿最后一关，没有 level_N.json 可进，回主菜单
        if self.game_info[c.LEVEL_NUM] >= c.LEVEL_COUNT:
            return c.MAIN_MENU
        return c.LEVEL
    
    def playMusic(self):
        tool.music_manager.play_music(c.MUSIC_VICTORY, loops=0)

class GameLoseScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
    
    def getImageName(self):
        return c.GAME_LOSE_IMAGE
    
    def set_next_state(self):
        # 如果是从关卡选择进入的，返回关卡选择界面
        if self.game_info.get('from_level_select', False):
            return c.LEVEL_SELECT
        return c.MAIN_MENU
    
    def playMusic(self):
        tool.music_manager.play_music(c.MUSIC_LOSE, loops=0)