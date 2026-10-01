"""Explosive plants - plants that explode to damage zombies."""
__author__ = 'marble_xu'

from ... import tool
from ... import constants as c
from .base import Plant


class CherryBomb(Plant):
    """Explosive plant that damages all zombies in a 3x3 area."""
    
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.CHERRYBOMB, c.WALLNUT_HEALTH, None)
        self.state = c.ATTACK
        self.start_boom = False
        self.bomb_timer = 0
        self.explode_y_range = c.CHERRYBOMB_EXPLODE_Y_RANGE
        self.explode_x_range = c.CHERRYBOMB_EXPLODE_X_RANGE
    
    def setBoom(self):
        frame = tool.GFX[c.CHERRY_BOOM_IMAGE]
        rect = frame.get_rect()
        width, height = rect.w, rect.h
                
        old_rect = self.rect
        image = tool.get_image(frame, 0, 0, width, height, c.BLACK, 1)
        self.image = image
        self.rect = image.get_rect()
        self.rect.centerx = old_rect.centerx
        self.rect.centery = old_rect.centery
        self.start_boom = True

    def animation(self):
        if self.start_boom:
            if self.bomb_timer == 0:
                self.bomb_timer = self.current_time
            elif(self.current_time - self.bomb_timer) > c.CHERRYBOMB_EXPLODE_TIME:
                self.health = 0
        else:
            if (self.current_time - self.animate_timer) > c.CHERRYBOMB_ANIMATE_INTERVAL:
                self.frame_index += 1
                if self.frame_index >= self.frame_num:
                    self.setBoom()
                    return
                self.animate_timer = self.current_time
            
            self.image = self.frames[self.frame_index]


class PotatoMine(Plant):
    """Mine that arms after a delay and explodes when zombies step on it."""
    
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.POTATOMINE, c.PLANT_HEALTH, None)
        self.animate_interval = c.POTATOMINE_ANIMATE_INTERVAL
        self.is_init = True
        self.init_timer = 0
        self.bomb_timer = 0
        self.explode_y_range = 0
        self.explode_x_range = c.POTATOMINE_EXPLODE_X_RANGE

    def loadImages(self, name, scale):
        self.init_frames = []
        self.idle_frames = []
        self.explode_frames = []
        
        init_name = name + 'Init'
        idle_name = name
        explode_name = name + 'Explode'
        
        frame_list = [self.init_frames, self.idle_frames, self.explode_frames]
        name_list = [init_name, idle_name, explode_name]

        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, 1, c.WHITE)

        self.frames = self.init_frames

    def idling(self):
        if self.is_init:
            if self.init_timer == 0:
                self.init_timer = self.current_time
            elif (self.current_time - self.init_timer) > c.POTATOMINE_INIT_TIME:
                self.changeFrames(self.idle_frames)
                self.is_init = False

    def canAttack(self, zombie):
        if not self.is_init and zombie.state != c.DIE:
            # Check if zombie is stepping on the potato mine
            # Zombie's right edge should overlap with potato mine
            if (zombie.rect.right >= self.rect.left and 
                zombie.rect.left <= self.rect.right):
                return True
        return False

    def attacking(self):
        if self.bomb_timer == 0:
            self.bomb_timer = self.current_time
            self.changeFrames(self.explode_frames)
        elif (self.current_time - self.bomb_timer) > c.POTATOMINE_EXPLODE_TIME:
            self.health = 0


class Jalapeno(Plant):
    """Explosive plant that damages entire row with fire."""
    
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.JALAPENO, c.PLANT_HEALTH, None)
        self.orig_pos = (x, y)
        self.state = c.ATTACK
        self.start_explode = False
        self.explode_y_range = 0
        self.explode_x_range = c.JALAPENO_EXPLODE_X_RANGE
        
    def loadImages(self, name, scale):
        self.explode_frames = []
        explode_name = name + 'Explode'
        self.loadFrames(self.explode_frames, explode_name, 1, c.WHITE)
        
        self.loadFrames(self.frames, name, 1, c.WHITE)

    def setExplode(self):
        self.changeFrames(self.explode_frames)
        self.animate_timer = self.current_time
        self.rect.x = c.MAP_OFFSET_X
        self.start_explode = True

    def animation(self):
        if self.start_explode:
            if(self.current_time - self.animate_timer) > c.JALAPENO_ANIMATE_INTERVAL:
                self.frame_index += 1
                if self.frame_index >= self.frame_num:
                    self.health = 0
                    return
                self.animate_timer = self.current_time
        else:
            if (self.current_time - self.animate_timer) > c.JALAPENO_ANIMATE_INTERVAL:
                self.frame_index += 1
                if self.frame_index >= self.frame_num:
                    self.setExplode()
                    return
                self.animate_timer = self.current_time
        self.image = self.frames[self.frame_index]

    def getPosition(self):
        return self.orig_pos
