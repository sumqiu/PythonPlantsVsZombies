"""Special zombies with unique behaviors and abilities."""

__author__ = 'marble_xu'

from .base import Zombie
from ... import tool
from ... import constants as c


class NewspaperZombie(Zombie):
    """Zombie reading a newspaper that speeds up when the paper is destroyed."""
    
    def __init__(self, x, y, head_group):
        Zombie.__init__(self, x, y, c.NEWSPAPER_ZOMBIE, c.NEWSPAPER_HEALTH, head_group)
        self.helmet = True

    def loadImages(self):
        self.helmet_walk_frames = []
        self.helmet_attack_frames = []
        self.walk_frames = []
        self.attack_frames = []
        self.losthead_walk_frames = []
        self.losthead_attack_frames = []
        self.die_frames = []
        self.boomdie_frames = []

        helmet_walk_name = self.name
        helmet_attack_name = self.name + 'Attack'
        walk_name = self.name + 'NoPaper'
        attack_name = self.name + 'NoPaperAttack'
        losthead_walk_name = self.name + 'LostHead'
        losthead_attack_name = self.name + 'LostHeadAttack'
        die_name = self.name + 'Die'
        boomdie_name = c.BOOMDIE

        frame_list = [self.helmet_walk_frames, self.helmet_attack_frames,
                      self.walk_frames, self.attack_frames, self.losthead_walk_frames,
                      self.losthead_attack_frames, self.die_frames, self.boomdie_frames]
        name_list = [helmet_walk_name, helmet_attack_name,
                     walk_name, attack_name, losthead_walk_name,
                     losthead_attack_name, die_name, boomdie_name]

        for i, name in enumerate(name_list):
            if name == c.BOOMDIE:
                color = c.BLACK
            else:
                color = c.WHITE
            self.loadFrames(frame_list[i], name, tool.ZOMBIE_RECT[name]['x'], color)

        self.frames = self.helmet_walk_frames
