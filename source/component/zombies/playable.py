"""Playable zombies that can be placed by the player and attack from left to right."""

__author__ = 'marble_xu'

import pygame as pg
from .base import Zombie
from ... import tool
from ... import constants as c

# Class-level cache: (ClassName, attr_name) -> [flipped Surface, ...]
# Shared across all instances of the same type so each frame is only flipped once.
_flipped_cache = {}

_MIRROR_ATTRS = (
    'helmet_walk_frames', 'helmet_attack_frames',
    'walk_frames', 'attack_frames',
    'losthead_walk_frames', 'losthead_attack_frames',
    'die_frames', 'boomdie_frames',
)


class PlayableZombie(Zombie):
    """Base class for zombies that can be placed by the player.
    These zombies move from left to right and attack plants."""
    
    def __init__(self, x, y, name, health, head_group=None, damage=1, has_helmet=False):
        # Initialize as a regular zombie first
        super().__init__(x, y, name, health, head_group, damage)
        # Mark as player-controlled (attacks right)
        self.is_playable = True
        # Set helmet status (will be used in mirrorAllFrames)
        self.helmet = has_helmet
        # Mirror all frames horizontally
        self.mirrorAllFrames()
    
    def mirrorAllFrames(self):
        """Mirror all zombie frames horizontally using a class-level cache.

        The first instance of each subclass pays the flip cost; every subsequent
        instance simply reuses the already-flipped surfaces stored in
        _flipped_cache[(ClassName, attr)], avoiding redundant work and memory.
        """
        class_name = type(self).__name__
        for attr in _MIRROR_ATTRS:
            if not hasattr(self, attr):
                continue
            key = (class_name, attr)
            if key not in _flipped_cache:
                _flipped_cache[key] = [
                    pg.transform.flip(f, True, False) for f in getattr(self, attr)
                ]
            setattr(self, attr, _flipped_cache[key])

        if hasattr(self, 'helmet_walk_frames') and self.helmet:
            self.frames = self.helmet_walk_frames
        else:
            self.frames = self.walk_frames

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
    
    def walking(self):
        """Override walking to move right instead of left."""
        if self.health <= 0:
            self.setDie()
        elif self.health <= c.LOSTHEAD_HEALTH and not self.losHead:
            self.changeFrames(self.losthead_walk_frames)
            self.setLostHead()
        elif self.health <= c.NORMAL_HEALTH and self.helmet:
            self.changeFrames(self.walk_frames)
            self.helmet = False

        if (self.current_time - self.walk_timer) > (c.ZOMBIE_WALK_INTERVAL * self.getTimeRatio()):
            self.walk_timer = self.current_time
            # Move right instead of left
            self.rect.x += self.speed
    
    def animation(self):
        """Override animation to not flip the image (already mirrored).

        Shared cached surfaces must never have set_alpha called on them directly,
        as that would affect every other instance reusing the same Surface.
        A lightweight copy() is made only for the two cases that need alpha:
        freeze tint and brief hit-flash.
        """
        if self.state == c.FREEZE:
            self.image = self.frames[self.frame_index].copy()
            self.image.set_alpha(192)
            return

        if (self.current_time - self.animate_timer) > (self.animate_interval * self.getTimeRatio()):
            self.frame_index += 1
            if self.frame_index >= self.frame_num:
                if self.state == c.DIE:
                    self.kill()
                    return
                self.frame_index = 0
            self.animate_timer = self.current_time

        frame = self.frames[self.frame_index]
        if (self.current_time - self.hit_timer) < c.PLANT_HIT_FLASH_TIME:
            self.image = frame.copy()
            self.image.set_alpha(c.PLANT_ALPHA_HIT)
        else:
            self.image = frame
    
    def canAttack(self, zombie):
        """Check if this playable zombie can attack another zombie."""
        if (zombie.state != c.DIE and self.rect.right >= zombie.rect.x):
            return True
        return False


class PlayableBucketHeadZombie(PlayableZombie):
    """Playable version of the bucket head zombie."""
    
    def __init__(self, x, y, head_group):
        # Use same stats as regular bucket head zombie, with helmet
        PlayableZombie.__init__(self, x, y, c.BUCKETHEAD_ZOMBIE, c.BUCKETHEAD_HEALTH, head_group, damage=1, has_helmet=True)

    def loadImages(self):
        self._load_helmeted_images()


class PlayableConeHeadZombie(PlayableZombie):
    """Playable version of the cone head zombie."""
    
    def __init__(self, x, y, head_group):
        # Use same stats as regular cone head zombie, with helmet
        PlayableZombie.__init__(self, x, y, c.CONEHEAD_ZOMBIE, c.CONEHEAD_HEALTH, head_group, damage=1, has_helmet=True)

    def loadImages(self):
        self._load_helmeted_images()


class PlayableNormalZombie(PlayableZombie):
    """Playable version of the normal zombie."""
    
    def __init__(self, x, y, head_group):
        PlayableZombie.__init__(self, x, y, c.NORMAL_ZOMBIE, c.NORMAL_HEALTH, head_group, damage=1)

    def loadImages(self):
        """Load all animation frames."""
        self.walk_frames = []
        self.attack_frames = []
        self.losthead_walk_frames = []
        self.losthead_attack_frames = []
        self.die_frames = []
        self.boomdie_frames = []

        walk_name = self.name
        attack_name = self.name + 'Attack'
        losthead_walk_name = self.name + 'LostHead'
        losthead_attack_name = self.name + 'LostHeadAttack'
        die_name = self.name + 'Die'
        boomdie_name = c.BOOMDIE

        frame_list = [self.walk_frames, self.attack_frames, self.losthead_walk_frames,
                      self.losthead_attack_frames, self.die_frames, self.boomdie_frames]
        name_list = [walk_name, attack_name, losthead_walk_name,
                     losthead_attack_name, die_name, boomdie_name]
        
        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, tool.ZOMBIE_RECT[name]['x'])

        self.frames = self.walk_frames
