"""Defensive plants - plants that block or damage zombies passively."""
__author__ = 'marble_xu'

from ... import constants as c
from .base import Plant


class WallNut(Plant):
    """Defensive plant with high health that blocks zombies."""
    
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.WALLNUT, c.WALLNUT_HEALTH, None)
        self.load_images()
        self.cracked1 = False
        self.cracked2 = False

    def load_images(self):
        self.cracked1_frames = []
        self.cracked2_frames = []
        
        cracked1_frames_name = self.name + '_cracked1'
        cracked2_frames_name = self.name + '_cracked2'

        self.loadFrames(self.cracked1_frames, cracked1_frames_name, 1)
        self.loadFrames(self.cracked2_frames, cracked2_frames_name, 1)
    
    def idling(self):
        if not self.cracked1 and self.health <= c.WALLNUT_CRACKED1_HEALTH:
            self.changeFrames(self.cracked1_frames)
            self.cracked1 = True
        elif not self.cracked2 and self.health <= c.WALLNUT_CRACKED2_HEALTH:
            self.changeFrames(self.cracked2_frames)
            self.cracked2 = True


class Spikeweed(Plant):
    """Ground plant that damages zombies walking over it."""
    
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.SPIKEWEED, c.PLANT_HEALTH, None)
        self.animate_interval = c.SPIKEWEED_ANIMATE_INTERVAL_IDLE
        self.attack_timer = 0

    def loadImages(self, name, scale):
        self.loadFrames(self.frames, name, 0.9, c.WHITE)

    def setIdle(self):
        self.animate_interval = c.SPIKEWEED_ANIMATE_INTERVAL_IDLE
        self.state = c.IDLE

    def canAttack(self, zombie):
        if (self.rect.x <= zombie.rect.right and
            (self.rect.right >= zombie.rect.x)):
            return True
        return False

    def setAttack(self, zombie_group):
        self.zombie_group = zombie_group
        self.animate_interval = c.SPIKEWEED_ANIMATE_INTERVAL_ATTACK
        self.state = c.ATTACK

    def attacking(self):
        if (self.current_time - self.attack_timer) > c.SPIKEWEED_ATTACK_INTERVAL:
            self.attack_timer = self.current_time
            for zombie in self.zombie_group:
                # Skip playable zombies (player's zombies)
                if hasattr(zombie, 'is_playable') and zombie.is_playable:
                    continue
                if self.canAttack(zombie):
                    zombie.setDamage(1, False)
