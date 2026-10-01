"""Special function plants - plants with unique abilities."""
__author__ = 'marble_xu'

from ... import constants as c
from .base import Plant, Sun


class SunFlower(Plant):
    """Plant that produces sun resources."""
    
    def __init__(self, x, y, sun_group):
        Plant.__init__(self, x, y, c.SUNFLOWER, c.PLANT_HEALTH, None)
        self.sun_timer = 0
        self.sun_group = sun_group
    
    def idling(self):
        if self.sun_timer == 0:
            self.sun_timer = self.current_time - (c.FLOWER_SUN_INTERVAL - c.SUNFLOWER_INITIAL_TIMER_OFFSET)
        elif (self.current_time - self.sun_timer) > c.FLOWER_SUN_INTERVAL:
            self.sun_group.add(Sun(self.rect.centerx, self.rect.bottom, self.rect.right, self.rect.bottom + self.rect.h // 2))
            self.sun_timer = self.current_time


class Chomper(Plant):
    """Plant that eats zombies whole but needs time to digest."""
    
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.CHOMPER, c.PLANT_HEALTH, None)
        self.animate_interval = c.CHOMPER_ANIMATE_INTERVAL
        self.digest_timer = 0
        self.digest_interval = c.CHOMPER_DIGEST_INTERVAL
        self.attack_zombie = None
        self.zombie_group = None

    def loadImages(self, name, scale):
        self.idle_frames = []
        self.attack_frames = []
        self.digest_frames = []

        idle_name = name
        attack_name = name + 'Attack'
        digest_name = name + 'Digest'

        frame_list = [self.idle_frames, self.attack_frames, self.digest_frames]
        name_list = [idle_name, attack_name, digest_name]
        scale_list = [1, 1, 1]
        rect_list = [(0, 0, 100, 114), None, None]

        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, scale_list[i])

        self.frames = self.idle_frames

    def canAttack(self, zombie):
        if (self.state == c.IDLE and zombie.state != c.DIGEST and
            self.rect.x <= zombie.rect.right and
            (self.rect.right + c.CHOMPER_ATTACK_X_RANGE >= zombie.rect.x)):
            return True
        return False

    def setIdle(self):
        self.state = c.IDLE
        self.changeFrames(self.idle_frames)

    def setAttack(self, zombie, zombie_group):
        self.attack_zombie = zombie
        self.zombie_group = zombie_group
        self.state = c.ATTACK
        self.changeFrames(self.attack_frames)

    def setDigest(self):
        self.state = c.DIGEST
        self.changeFrames(self.digest_frames)

    def attacking(self):
        if self.frame_index == (self.frame_num - 3):
            self.zombie_group.remove(self.attack_zombie)
        if (self.frame_index + 1) == self.frame_num:
            self.setDigest()

    def digest(self):
        if self.digest_timer == 0:
            self.digest_timer = self.current_time
        elif (self.current_time - self.digest_timer) > self.digest_interval:
            self.digest_timer = 0
            self.attack_zombie.kill()
            self.setIdle()


class Squash(Plant):
    """Plant that jumps on and squashes zombies."""
    
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.SQUASH, c.PLANT_HEALTH, None)
        self.orig_pos = (x, y)
        self.aim_timer = 0
        self.squashing = False

    def loadImages(self, name, scale):
        self.idle_frames = []
        self.aim_frames = []
        self.attack_frames = []
        
        idle_name = name
        aim_name = name + 'Aim'
        attack_name = name + 'Attack'
        
        frame_list = [self.idle_frames, self.aim_frames, self.attack_frames]
        name_list = [idle_name, aim_name, attack_name]

        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, 1, c.WHITE)

        self.frames = self.idle_frames

    def canAttack(self, zombie):
        if (self.state == c.IDLE and self.rect.x <= zombie.rect.right and
            (self.rect.right + c.SQUASH_ATTACK_RANGE >= zombie.rect.x)):
            return True
        return False

    def setAttack(self, zombie, zombie_group):
        self.attack_zombie = zombie
        self.zombie_group = zombie_group
        self.state = c.ATTACK

    def attacking(self):
        if self.squashing:
            if self.frame_index == 2:
                self.zombie_group.remove(self.attack_zombie)
            if (self.frame_index + 1) == self.frame_num:
                self.attack_zombie.kill()
                self.health = 0
        elif self.aim_timer == 0:
            self.aim_timer = self.current_time
            self.changeFrames(self.aim_frames)
        elif (self.current_time - self.aim_timer) > c.SQUASH_AIM_TIME:
            self.changeFrames(self.attack_frames)
            self.rect.centerx = self.attack_zombie.rect.centerx
            self.squashing = True
            self.animate_interval = c.SQUASH_ANIMATE_INTERVAL

    def getPosition(self):
        return self.orig_pos
