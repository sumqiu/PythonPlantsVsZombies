"""Armored zombies with helmets providing extra protection."""

__author__ = 'marble_xu'

from .base import Zombie
from ... import constants as c


class ConeHeadZombie(Zombie):
    """Zombie wearing a traffic cone for extra protection."""
    
    def __init__(self, x, y, head_group):
        Zombie.__init__(self, x, y, c.CONEHEAD_ZOMBIE, c.CONEHEAD_HEALTH, head_group)
        self.helmet = True

    def loadImages(self):
        self._load_helmeted_images()


class BucketHeadZombie(Zombie):
    """Zombie wearing a bucket for maximum protection."""
    
    def __init__(self, x, y, head_group):
        Zombie.__init__(self, x, y, c.BUCKETHEAD_ZOMBIE, c.BUCKETHEAD_HEALTH, head_group)
        self.helmet = True

    def loadImages(self):
        self._load_helmeted_images()
