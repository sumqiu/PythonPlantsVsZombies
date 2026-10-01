"""Mushroom type plants - plants that can sleep during day."""
__author__ = 'marble_xu'

from ... import constants as c
from .base import Plant, Bullet, Sun


class PuffShroom(Plant):
    """Small mushroom that shoots short-range spores."""
    
    def __init__(self, x, y, bullet_group):
        Plant.__init__(self, x, y, c.PUFFSHROOM, c.PLANT_HEALTH, bullet_group)
        self.can_sleep = True
        self.shoot_timer = 0

    def loadImages(self, name, scale):
        self.idle_frames = []
        self.sleep_frames = []

        idle_name = name
        sleep_name = name + 'Sleep'
        
        frame_list = [self.idle_frames, self.sleep_frames]
        name_list = [idle_name, sleep_name]

        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, 1)

        self.frames = self.idle_frames

    def attacking(self):
        if (self.current_time - self.shoot_timer) > c.PUFFSHROOM_SHOOT_INTERVAL:
            self.bullet_group.add(Bullet(self.rect.right, self.rect.y + c.PUFFSHROOM_BULLET_OFFSET_Y, self.rect.y + c.PUFFSHROOM_BULLET_OFFSET_Y,
                                    c.BULLET_MUSHROOM, c.BULLET_DAMAGE_NORMAL, True))
            self.shoot_timer = self.current_time

    def canAttack(self, zombie):
        if (self.rect.x <= zombie.rect.right and
            (self.rect.right + c.PUFFSHROOM_ATTACK_RANGE >= zombie.rect.x)):
            return True
        return False


class ScaredyShroom(Plant):
    """Mushroom that hides when zombies get too close."""
    
    def __init__(self, x, y, bullet_group):
        Plant.__init__(self, x, y, c.SCAREDYSHROOM, c.PLANT_HEALTH, bullet_group)
        self.can_sleep = True
        self.shoot_timer = 0
        self.cry_x_range = c.SCAREDYSHROOM_CRY_X_RANGE

    def loadImages(self, name, scale):
        self.idle_frames = []
        self.cry_frames = []
        self.sleep_frames = []

        idle_name = name
        cry_name = name + 'Cry'
        sleep_name = name + 'Sleep'
        
        frame_list = [self.idle_frames, self.cry_frames, self.sleep_frames]
        name_list = [idle_name, cry_name, sleep_name]

        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, 1, c.WHITE)

        self.frames = self.idle_frames

    def needCry(self, zombie):
        if (zombie.state != c.DIE and self.rect.x <= zombie.rect.right and 
            self.rect.x + self.cry_x_range > zombie.rect.x):
            return True
        return False

    def setCry(self):
        self.state = c.CRY
        self.changeFrames(self.cry_frames)

    def setAttack(self):
        self.state = c.ATTACK
        self.changeFrames(self.idle_frames)

    def setIdle(self):
        self.state = c.IDLE
        self.changeFrames(self.idle_frames)

    def attacking(self):
        if (self.current_time - self.shoot_timer) > c.SCAREDYSHROOM_SHOOT_INTERVAL:
            self.bullet_group.add(Bullet(self.rect.right, self.rect.y + c.SCAREDYSHROOM_BULLET_OFFSET_Y, self.rect.y + c.SCAREDYSHROOM_BULLET_OFFSET_Y,
                                    c.BULLET_MUSHROOM, c.BULLET_DAMAGE_NORMAL, True))
            self.shoot_timer = self.current_time


class SunShroom(Plant):
    """Mushroom that produces sun, grows bigger over time."""
    
    def __init__(self, x, y, sun_group):
        Plant.__init__(self, x, y, c.SUNSHROOM, c.PLANT_HEALTH, None)
        self.can_sleep = True
        self.animate_interval = c.SUNSHROOM_ANIMATE_INTERVAL
        self.sun_timer = 0
        self.sun_group = sun_group
        self.is_big = False
        self.change_timer = 0

    def loadImages(self, name, scale):
        self.idle_frames = []
        self.big_frames = []
        self.sleep_frames = []

        idle_name = name
        big_name = name + 'Big'
        sleep_name = name + 'Sleep'
        
        frame_list = [self.idle_frames, self.big_frames, self.sleep_frames]
        name_list = [idle_name, big_name, sleep_name]

        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, 1, c.WHITE)

        self.frames = self.idle_frames

    def idling(self):
        if not self.is_big:
            if self.change_timer == 0:
                self.change_timer = self.current_time
            elif (self.current_time - self.change_timer) > c.SUNSHROOM_GROW_TIME:
                self.changeFrames(self.big_frames)
                self.is_big = True
        
        if self.sun_timer == 0:
            self.sun_timer = self.current_time - (c.FLOWER_SUN_INTERVAL - 6000)
        elif (self.current_time - self.sun_timer) > c.FLOWER_SUN_INTERVAL:
            self.sun_group.add(Sun(self.rect.centerx, self.rect.bottom, self.rect.right,
                                   self.rect.bottom + self.rect.h // 2, self.is_big))
            self.sun_timer = self.current_time


class IceShroom(Plant):
    """Mushroom that freezes all zombies on screen."""
    
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.ICESHROOM, c.PLANT_HEALTH, None)
        self.can_sleep = True
        self.orig_pos = (x, y)
        self.start_freeze = False

    def loadImages(self, name, scale):
        self.idle_frames = []
        self.snow_frames = []
        self.sleep_frames = []
        self.trap_frames = []

        idle_name = name
        snow_name = name + 'Snow'
        sleep_name = name + 'Sleep'
        trap_name = name + 'Trap'
        
        frame_list = [self.idle_frames, self.snow_frames, self.sleep_frames, self.trap_frames]
        name_list = [idle_name, snow_name, sleep_name, trap_name]
        scale_list = [1, 1.5, 1, 1]

        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, scale_list[i], c.WHITE)

        self.frames = self.idle_frames

    def setFreeze(self):
        self.changeFrames(self.snow_frames)
        self.animate_timer = self.current_time
        self.rect.x = c.MAP_OFFSET_X
        self.rect.y = c.MAP_OFFSET_Y
        self.start_freeze = True

    def animation(self):
        if self.start_freeze:
            if(self.current_time - self.animate_timer) > c.ICESHROOM_ANIMATE_INTERVAL_FREEZE:
                self.frame_index += 1
                if self.frame_index >= self.frame_num:
                    self.health = 0
                    return
                self.animate_timer = self.current_time
        else:
            if (self.current_time - self.animate_timer) > c.ICESHROOM_ANIMATE_INTERVAL_IDLE:
                self.frame_index += 1
                if self.frame_index >= self.frame_num:
                    if self.state == c.SLEEP:
                        self.frame_index = 0
                    else:
                        self.setFreeze()
                        return
                self.animate_timer = self.current_time
        self.image = self.frames[self.frame_index]

    def getPosition(self):
        return self.orig_pos


class HypnoShroom(Plant):
    """Mushroom that hypnotizes zombies to fight for plants."""
    
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.HYPNOSHROOM, 1, None)
        self.can_sleep = True
        self.animate_interval = c.HYPNOSHROOM_ANIMATE_INTERVAL

    def loadImages(self, name, scale):
        self.idle_frames = []
        self.sleep_frames = []

        idle_name = name
        sleep_name = name + 'Sleep'

        frame_list = [self.idle_frames, self.sleep_frames]
        name_list = [idle_name, sleep_name]

        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, 1, c.WHITE)

        self.frames = self.idle_frames
