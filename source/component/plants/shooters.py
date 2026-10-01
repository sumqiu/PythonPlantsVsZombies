"""Shooter type plants - plants that fire projectiles."""
__author__ = 'marble_xu'

from ... import constants as c
from .base import Plant, Bullet


class PeaShooter(Plant):
    """Plant that shoots peas at zombies."""
    
    def __init__(self, x, y, bullet_group):
        Plant.__init__(self, x, y, c.PEASHOOTER, c.PLANT_HEALTH, bullet_group)
        self.shoot_timer = 0
        
    def attacking(self):
        if (self.current_time - self.shoot_timer) > c.PLANT_SHOOT_INTERVAL:
            self.bullet_group.add(Bullet(self.rect.right, self.rect.y, self.rect.y,
                                    c.BULLET_PEA, c.BULLET_DAMAGE_NORMAL, False))
            self.shoot_timer = self.current_time


class RepeaterPea(Plant):
    """Plant that shoots two peas in succession."""
    
    def __init__(self, x, y, bullet_group):
        Plant.__init__(self, x, y, c.REPEATERPEA, c.PLANT_HEALTH, bullet_group)
        self.shoot_timer = 0

    def attacking(self):
        if (self.current_time - self.shoot_timer) > c.PLANT_SHOOT_INTERVAL:
            self.bullet_group.add(Bullet(self.rect.right, self.rect.y, self.rect.y,
                                    c.BULLET_PEA, c.BULLET_DAMAGE_NORMAL, False))
            self.bullet_group.add(Bullet(self.rect.right + c.REPEATERPEA_BULLET_OFFSET_X, self.rect.y, self.rect.y,
                                    c.BULLET_PEA, c.BULLET_DAMAGE_NORMAL, False))
            self.shoot_timer = self.current_time


class ThreePeaShooter(Plant):
    """Plant that shoots peas in three directions."""
    
    def __init__(self, x, y, bullet_groups, map_y):
        Plant.__init__(self, x, y, c.THREEPEASHOOTER, c.PLANT_HEALTH, None)
        self.shoot_timer = 0
        self.map_y = map_y
        self.bullet_groups = bullet_groups

    def attacking(self):
        if (self.current_time - self.shoot_timer) > c.PLANT_SHOOT_INTERVAL:
            for i in range(3):
                tmp_y = self.map_y + (i - 1)
                if tmp_y < 0 or tmp_y >= c.GRID_Y_LEN:
                    continue
                dest_y = self.rect.y + (i - 1) * c.GRID_Y_SIZE + c.THREEPEASHOOTER_BULLET_OFFSET_Y
                self.bullet_groups[tmp_y].add(Bullet(self.rect.right, self.rect.y, dest_y,
                                        c.BULLET_PEA, c.BULLET_DAMAGE_NORMAL, False))
            self.shoot_timer = self.current_time


class SnowPeaShooter(Plant):
    """Plant that shoots freezing peas."""
    
    def __init__(self, x, y, bullet_group):
        Plant.__init__(self, x, y, c.SNOWPEASHOOTER, c.PLANT_HEALTH, bullet_group)
        self.shoot_timer = 0

    def attacking(self):
        if (self.current_time - self.shoot_timer) > c.PLANT_SHOOT_INTERVAL:
            self.bullet_group.add(Bullet(self.rect.right, self.rect.y, self.rect.y,
                                    c.BULLET_PEA_ICE, c.BULLET_DAMAGE_NORMAL, True))
            self.shoot_timer = self.current_time
