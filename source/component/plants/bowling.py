"""Bowling mode plants - special plants for bowling mini-game."""
__author__ = 'marble_xu'

import random
import pygame as pg
from ... import constants as c
from .base import Plant


class WallNutBowling(Plant):
    """Rolling wallnut that damages zombies in bowling mode."""
    
    def __init__(self, x, y, map_y, level):
        Plant.__init__(self, x, y, c.WALLNUTBOWLING, 1, None)
        self.map_y = map_y
        self.level = level
        self.init_rect = self.rect.copy()
        self.rotate_degree = 0
        self.animate_interval = c.WALLNUTBOWLING_ANIMATE_INTERVAL
        self.move_timer = 0
        self.move_interval = c.WALLNUTBOWLING_MOVE_INTERVAL
        self.vel_x = random.randint(12, 15)
        self.vel_y = 0
        self.disable_hit_y = -1

    def loadImages(self, name, scale):
        self.loadFrames(self.frames, name, 1, c.WHITE)

    def idling(self):
        if self.move_timer == 0:
            self.move_timer = self.current_time
        elif (self.current_time - self.move_timer) >= self.move_interval:
            self.rotate_degree = (self.rotate_degree - c.WALLNUTBOWLING_ROTATE_DEGREE) % 360
            self.init_rect.x += self.vel_x
            self.init_rect.y += self.vel_y
            self.handleMapYPosition()
            if self.shouldChangeDirection():
                self.changeDirection(-1)
            if self.init_rect.x > c.SCREEN_WIDTH:
                self.health = 0
            self.move_timer += self.move_interval

    def canHit(self, map_y):
        if self.disable_hit_y == map_y:
            return False
        return True

    def handleMapYPosition(self):
        _, map_y1 = self.level.map.getMapIndex(self.init_rect.x, self.init_rect.centery)
        _, map_y2 = self.level.map.getMapIndex(self.init_rect.x, self.init_rect.bottom)
        if self.map_y != map_y1 and map_y1 == map_y2:
            # wallnut bowls to another row, should modify which plant group it belongs to
            self.level.plant_groups[self.map_y].remove(self)
            self.level.plant_groups[map_y1].add(self)
            self.map_y = map_y1

    def shouldChangeDirection(self):
        if self.init_rect.centery <= c.MAP_OFFSET_Y:
            return True
        elif self.init_rect.bottom + 20 >= c.SCREEN_HEIGHT:
            return True
        return False

    def changeDirection(self, map_y):
        if self.vel_y == 0:
            if self.map_y == 0:
                direc = 1
            elif self.map_y == (c.GRID_Y_LEN-1):
                direc = -1
            else:
                if random.randint(0, 1) == 0:
                    direc = 1
                else:
                    direc = -1
            self.vel_y = self.vel_x * direc
        else:
            self.vel_y = - self.vel_y

        # map_y < 0 表示是撞到屏幕上/下边界弹回来的（见 shouldChangeDirection），
        # 那不是"刚打过某一排"，所以不能写进 disable_hit_y。
        if map_y >= 0:
            self.disable_hit_y = map_y

    def animation(self):
        if (self.current_time - self.animate_timer) > self.animate_interval:
            self.frame_index += 1
            if self.frame_index >= self.frame_num:
                self.frame_index = 0
            self.animate_timer = self.current_time
            
        image = self.frames[self.frame_index]
        self.image = pg.transform.rotate(image, self.rotate_degree)
        # must keep the center postion of image when rotate
        self.rect = self.image.get_rect(center=self.init_rect.center)


class RedWallNutBowling(Plant):
    """Explosive rolling wallnut for bowling mode."""
    
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.REDWALLNUTBOWLING, 1, None)
        self.orig_y = y
        self.explode_timer = 0
        self.explode_y_range = 1
        self.explode_x_range = c.GRID_X_SIZE
        self.init_rect = self.rect.copy()
        self.rotate_degree = 0
        self.animate_interval = c.WALLNUTBOWLING_ANIMATE_INTERVAL
        self.move_timer = 0
        self.move_interval = c.WALLNUTBOWLING_MOVE_INTERVAL
        self.vel_x = random.randint(12, 15)

    def loadImages(self, name, scale):
        self.idle_frames = []
        self.explode_frames = []

        idle_name = name
        explode_name = name + 'Explode'
        
        frame_list = [self.idle_frames, self.explode_frames]
        name_list = [idle_name, explode_name]
        
        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, 1, c.WHITE)

        self.frames = self.idle_frames

    def idling(self):
        if self.move_timer == 0:
            self.move_timer = self.current_time
        elif (self.current_time - self.move_timer) >= self.move_interval:
            self.rotate_degree = (self.rotate_degree - c.WALLNUTBOWLING_ROTATE_DEGREE) % 360
            self.init_rect.x += self.vel_x
            if self.init_rect.x > c.SCREEN_WIDTH:
                self.health = 0
            self.move_timer += self.move_interval

    def attacking(self):
        if self.explode_timer == 0:
            self.explode_timer = self.current_time
            self.changeFrames(self.explode_frames)
        elif (self.current_time - self.explode_timer) > 500:
            self.health = 0

    def animation(self):
        if (self.current_time - self.animate_timer) > self.animate_interval:
            self.frame_index += 1
            if self.frame_index >= self.frame_num:
                self.frame_index = 0
            self.animate_timer = self.current_time

        image = self.frames[self.frame_index]
        if self.state == c.IDLE:
            self.image = pg.transform.rotate(image, self.rotate_degree)
        else:
            self.image = image
        # must keep the center postion of image when rotate
        self.rect = self.image.get_rect(center=self.init_rect.center)

    def getPosition(self):
        return (self.rect.centerx, self.orig_y)
