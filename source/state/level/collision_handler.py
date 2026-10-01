"""
Collision detection and handling
"""
import pygame as pg
from ... import constants as c


class CollisionHandler:
    def __init__(self, level):
        self.level = level
    
    def checkBulletCollisions(self):
        """Check bullet-zombie collisions"""
        collided_func = pg.sprite.collide_circle_ratio(0.7)
        for i in range(self.level.map_y_len):
            for bullet in self.level.bullet_groups[i]:
                if bullet.state == c.FLY:
                    zombie = pg.sprite.spritecollideany(bullet, self.level.zombie_groups[i], collided_func)
                    if zombie and zombie.state != c.DIE:
                        zombie.setDamage(bullet.damage, bullet.ice)
                        bullet.setExplode()
    
    def checkZombieCollisions(self):
        """Check zombie-plant collisions and playable zombie-zombie collisions"""
        if self.level.bar_type == c.CHOOSEBAR_BOWLING:
            ratio = 0.6
        else:
            ratio = 0.7
        collided_func = pg.sprite.collide_circle_ratio(ratio)
        
        for i in range(self.level.map_y_len):
            # Separate playable zombies from enemy zombies
            playable_zombies = []
            enemy_zombies = []
            
            for zombie in self.level.zombie_groups[i]:
                if hasattr(zombie, 'is_playable') and zombie.is_playable:
                    playable_zombies.append(zombie)
                else:
                    enemy_zombies.append(zombie)
            
            # Check enemy zombie vs plant collisions
            for zombie in enemy_zombies:
                if zombie.state != c.WALK:
                    continue
                plant = pg.sprite.spritecollideany(zombie, self.level.plant_groups[i], collided_func)
                if plant:
                    if plant.name == c.WALLNUTBOWLING:
                        if plant.canHit(i):
                            zombie.setDamage(c.WALLNUT_BOWLING_DAMAGE)
                            plant.changeDirection(i)
                    elif plant.name == c.REDWALLNUTBOWLING:
                        if plant.state == c.IDLE:
                            plant.setAttack()
                    elif plant.name != c.SPIKEWEED:
                        zombie.setAttack(plant)
            
            # Check playable zombie vs enemy zombie collisions
            for playable_zombie in playable_zombies:
                if playable_zombie.health <= 0 or playable_zombie.state == c.DIE:
                    continue
                
                for enemy_zombie in enemy_zombies:
                    if enemy_zombie.health <= 0 or enemy_zombie.state == c.DIE:
                        continue
                    
                    # Check collision
                    if collided_func(playable_zombie, enemy_zombie):
                        # Both zombies attack each other
                        if playable_zombie.state == c.WALK:
                            playable_zombie.setAttack(enemy_zombie, False)
                        if enemy_zombie.state == c.WALK:
                            enemy_zombie.setAttack(playable_zombie, False)

            # Check hypno zombie collisions
            for hypno_zombie in self.level.hypno_zombie_groups[i]:
                if hypno_zombie.health <= 0:
                    continue
                zombie_list = pg.sprite.spritecollide(hypno_zombie,
                               self.level.zombie_groups[i], False, collided_func)
                for zombie in zombie_list:
                    if zombie.state == c.DIE:
                        continue
                    # Skip if it's a playable zombie (they're on the same side)
                    if hasattr(zombie, 'is_playable') and zombie.is_playable:
                        continue
                    if zombie.state == c.WALK:
                        zombie.setAttack(hypno_zombie, False)
                    if hypno_zombie.state == c.WALK:
                        hypno_zombie.setAttack(zombie, False)

    def checkCarCollisions(self):
        """Check car-zombie collisions"""
        collided_func = pg.sprite.collide_circle_ratio(0.8)
        # self.level.cars 是普通 list，边遍历边 remove 会漏掉元素，复制一份再删
        for car in list(self.level.cars):
            zombies = pg.sprite.spritecollide(car, self.level.zombie_groups[car.map_y], False, collided_func)
            for zombie in zombies:
                if zombie and zombie.state != c.DIE:
                    car.setWalk()
                    zombie.setDie()
            if car.dead:
                self.level.cars.remove(car)

    def checkAllCollisions(self):
        """Check all collision types"""
        self.checkBulletCollisions()
        self.checkZombieCollisions()
        self.checkCarCollisions()
