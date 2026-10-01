"""Base classes for plants, bullets, sun, and car."""
__author__ = 'marble_xu'

import pygame as pg
from ... import tool
from ... import constants as c


def _load_plant_frames(frames, name, scale=1, color=c.BLACK):
    """从 GFX 裁矩形并填充帧列表，被 Plant 和 Bullet 共用。"""
    frame_list = tool.GFX[name]
    if name in tool.PLANT_RECT:
        data = tool.PLANT_RECT[name]
        x, y, width, height = data['x'], data['y'], data['width'], data['height']
    else:
        x, y = 0, 0
        rect = frame_list[0].get_rect()
        width, height = rect.w, rect.h
    for frame in frame_list:
        frames.append(tool.get_image(frame, x, y, width, height, color, scale))


class Car(pg.sprite.Sprite):
    """Car that moves across the lawn when zombies reach the left side."""
    
    def __init__(self, x, y, map_y):
        pg.sprite.Sprite.__init__(self)

        rect = tool.GFX[c.CAR].get_rect()
        width, height = rect.w, rect.h
        self.image = tool.get_image(tool.GFX[c.CAR], 0, 0, width, height)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.map_y = map_y
        self.state = c.IDLE
        self.dead = False

    def update(self, game_info):
        self.current_time = game_info[c.CURRENT_TIME]
        if self.state == c.IDLE:
            pass
        elif self.state == c.WALK:
            self.rect.x += c.CAR_VELOCITY
        if self.rect.x > c.SCREEN_WIDTH:
            self.dead = True

    def setWalk(self):
        if self.state == c.IDLE:
            self.state = c.WALK

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Bullet(pg.sprite.Sprite):
    """Projectile fired by plants."""
    
    def __init__(self, x, start_y, dest_y, name, damage, ice):
        pg.sprite.Sprite.__init__(self)

        self.name = name
        self.frames = []
        self.frame_index = 0
        self.load_images()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = start_y
        self.dest_y = dest_y
        self.y_vel = c.BULLET_VELOCITY_Y if (dest_y > start_y) else -c.BULLET_VELOCITY_Y
        self.x_vel = c.BULLET_VELOCITY_X
        self.damage = damage
        self.ice = ice
        self.state = c.FLY
        self.current_time = 0

    def loadFrames(self, frames, name):
        _load_plant_frames(frames, name)
    
    def load_images(self):
        self.fly_frames = []
        self.explode_frames = []
        
        fly_name = self.name
        if self.name == c.BULLET_MUSHROOM:
            explode_name = 'BulletMushRoomExplode'
        else:
            explode_name = 'PeaNormalExplode'
        
        self.loadFrames(self.fly_frames, fly_name)
        self.loadFrames(self.explode_frames, explode_name)
        
        self.frames = self.fly_frames

    def update(self, game_info):
        self.current_time = game_info[c.CURRENT_TIME]
        if self.state == c.FLY:
            if self.rect.y != self.dest_y:
                self.rect.y += self.y_vel
                if self.y_vel * (self.dest_y - self.rect.y) < 0:
                    self.rect.y = self.dest_y
            self.rect.x += self.x_vel
            if self.rect.x > c.SCREEN_WIDTH:
                self.kill()
        elif self.state == c.EXPLODE:
            if(self.current_time - self.explode_timer) > c.BULLET_EXPLODE_TIME:
                self.kill()

    def setExplode(self):
        self.state = c.EXPLODE
        self.explode_timer = self.current_time
        self.frames = self.explode_frames
        self.image = self.frames[self.frame_index]

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Plant(pg.sprite.Sprite):
    """Base class for all plants in the game."""
    
    def __init__(self, x, y, name, health, bullet_group, scale=1):
        pg.sprite.Sprite.__init__(self)
        
        self.frames = []
        self.frame_index = 0
        self.loadImages(name, scale)
        self.frame_num = len(self.frames)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        
        self.name = name
        self.health = health
        self.state = c.IDLE
        self.bullet_group = bullet_group
        self.can_sleep = False
        self.animate_timer = 0
        self.animate_interval = c.ANIMATION_INTERVAL_DEFAULT
        self.hit_timer = 0
        self.current_time = 0  # setDamage() may run before the first update()
        # 记录啃掉自己的僵尸；只有被啃到时才会赋值，所以必须先给 None，
        # 否则被铲子/爆炸清理时读它会 AttributeError。
        self.kill_zombie = None

    def loadFrames(self, frames, name, scale=1, color=c.BLACK):
        _load_plant_frames(frames, name, scale, color)

    def loadImages(self, name, scale):
        self.loadFrames(self.frames, name, scale)

    def changeFrames(self, frames):
        """Change image frames and modify rect position."""
        self.frames = frames
        self.frame_num = len(self.frames)
        self.frame_index = 0
        
        bottom = self.rect.bottom
        x = self.rect.x
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.x = x

    def update(self, game_info):
        self.current_time = game_info[c.CURRENT_TIME]
        self.handleState()
        self.animation()
    
    def handleState(self):
        if self.state == c.IDLE:
            self.idling()
        elif self.state == c.ATTACK:
            self.attacking()
        elif self.state == c.DIGEST:
            self.digest()

    def idling(self):
        pass

    def attacking(self):
        pass

    def digest(self):
        pass

    def animation(self):
        if (self.current_time - self.animate_timer) > self.animate_interval:
            self.frame_index += 1
            if self.frame_index >= self.frame_num:
                self.frame_index = 0
            self.animate_timer = self.current_time
        
        self.image = self.frames[self.frame_index]
        if(self.current_time - self.hit_timer) >= c.PLANT_HIT_FLASH_TIME:
            self.image.set_alpha(c.PLANT_ALPHA_NORMAL)
        else:
            self.image.set_alpha(c.PLANT_ALPHA_HIT)

    def canAttack(self, zombie):
        if (self.state != c.SLEEP and zombie.state != c.DIE and
            self.rect.x <= zombie.rect.right):
            return True
        return False

    def setAttack(self):
        self.state = c.ATTACK

    def setIdle(self):
        self.state = c.IDLE
        self.is_attacked = False

    def setSleep(self):
        self.state = c.SLEEP
        self.changeFrames(self.sleep_frames)

    def setDamage(self, damage, zombie):
        self.health -= damage
        self.hit_timer = self.current_time
        if self.health <= 0:
            self.kill_zombie = zombie

    def getPosition(self):
        return self.rect.centerx, self.rect.bottom


class Sun(Plant):
    """Sun collectible that provides resources."""
    
    def __init__(self, x, y, dest_x, dest_y, is_big=True):
        if is_big:
            scale = c.SUN_SCALE_BIG
            self.sun_value = c.SUN_VALUE
        else:
            scale = c.SUN_SCALE_SMALL
            self.sun_value = c.SUN_VALUE_SMALL
        Plant.__init__(self, x, y, c.SUN, 0, None, scale)
        self.move_speed = c.SUN_MOVE_SPEED
        self.dest_x = dest_x
        self.dest_y = dest_y
        self.die_timer = 0

    def handleState(self):
        if self.rect.centerx != self.dest_x:
            self.rect.centerx += self.move_speed if self.rect.centerx < self.dest_x else -self.move_speed
        if self.rect.bottom != self.dest_y:
            self.rect.bottom += self.move_speed if self.rect.bottom < self.dest_y else -self.move_speed
        
        if self.rect.centerx == self.dest_x and self.rect.bottom == self.dest_y:
            if self.die_timer == 0:
                self.die_timer = self.current_time
            elif(self.current_time - self.die_timer) > c.SUN_LIVE_TIME:
                self.state = c.DIE
                self.kill()

    def checkCollision(self, x, y):
        if self.state == c.DIE:
            return False
        if(x >= self.rect.x and x <= self.rect.right and
           y >= self.rect.y and y <= self.rect.bottom):
            self.state = c.DIE
            self.kill()
            return True
        return False
