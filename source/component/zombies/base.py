__author__ = 'marble_xu'

import pygame as pg
from ... import tool
from ... import constants as c


class Zombie(pg.sprite.Sprite):
    """Base class for all zombies in the game."""
    
    def __init__(self, x, y, name, health, head_group=None, damage=1):
        pg.sprite.Sprite.__init__(self)
        
        self.name = name
        self.frames = []
        self.frame_index = 0
        self.loadImages()
        self.frame_num = len(self.frames)

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        
        self.health = health
        self.damage = damage
        self.dead = False
        self.losHead = False
        self.helmet = False
        self.head_group = head_group

        self.walk_timer = 0
        self.animate_timer = 0
        self.attack_timer = 0
        self.prey = None
        self.prey_is_plant = True
        self.current_time = 0  # Initialize current_time to avoid AttributeError
        self.state = c.WALK
        self.animate_interval = c.ZOMBIE_ANIMATE_INTERVAL_WALK
        self.ice_slow_ratio = 1
        self.ice_slow_timer = 0
        self.hit_timer = 0
        self.speed = c.ZOMBIE_SPEED_NORMAL
        self.freeze_timer = 0
        self.is_hypno = False  # the zombie is hypno and attacks other zombies when it ate a HypnoShroom
    
    def loadFrames(self, frames, name, image_x, colorkey=c.BLACK):
        frame_list = tool.GFX[name]
        rect = frame_list[0].get_rect()
        width, height = rect.w, rect.h
        width -= image_x

        for frame in frame_list:
            frames.append(tool.get_image(frame, image_x, 0, width, height, colorkey))

    def _load_helmeted_images(self):
        """加载标准头盔僵尸的全套动画帧（盔行走/攻击 + 普通僵尸行走/攻击/无头/死亡）。
        头盔帧名称使用 self.name；其余帧沿用普通僵尸资源。
        加载后将 self.frames 指向 self.helmet_walk_frames。
        """
        self.helmet_walk_frames = []
        self.helmet_attack_frames = []
        self.walk_frames = []
        self.attack_frames = []
        self.losthead_walk_frames = []
        self.losthead_attack_frames = []
        self.die_frames = []
        self.boomdie_frames = []

        name_map = [
            (self.helmet_walk_frames,    self.name),
            (self.helmet_attack_frames,  self.name + 'Attack'),
            (self.walk_frames,           c.NORMAL_ZOMBIE),
            (self.attack_frames,         c.NORMAL_ZOMBIE + 'Attack'),
            (self.losthead_walk_frames,  c.NORMAL_ZOMBIE + 'LostHead'),
            (self.losthead_attack_frames, c.NORMAL_ZOMBIE + 'LostHeadAttack'),
            (self.die_frames,            c.NORMAL_ZOMBIE + 'Die'),
            (self.boomdie_frames,        c.BOOMDIE),
        ]
        for frames, name in name_map:
            self.loadFrames(frames, name, tool.ZOMBIE_RECT[name]['x'])

        self.frames = self.helmet_walk_frames

    def update(self, game_info):
        self.current_time = game_info[c.CURRENT_TIME]
        self.handleState()
        self.updateIceSlow()
        self.animation()

    def handleState(self):
        if self.state == c.WALK:
            self.walking()
        elif self.state == c.ATTACK:
            self.attacking()
        elif self.state == c.DIE:
            self.dying()
        elif self.state == c.FREEZE:
            self.freezing()

    def walking(self):
        if self.health <= 0:
            self.setDie()
        elif self.health <= c.LOSTHEAD_HEALTH and not self.losHead:
            self.changeFrames(self.losthead_walk_frames)
            self.setLostHead()
        elif self.health <= c.NORMAL_HEALTH and self.helmet:
            self.changeFrames(self.walk_frames)
            self.helmet = False
            if self.name == c.NEWSPAPER_ZOMBIE:
                self.speed = c.ZOMBIE_SPEED_FAST

        if (self.current_time - self.walk_timer) > (c.ZOMBIE_WALK_INTERVAL * self.getTimeRatio()):
            self.walk_timer = self.current_time
            if self.is_hypno:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed
    
    def attacking(self):
        if self.health <= 0:
            self.setDie()
        elif self.health <= c.LOSTHEAD_HEALTH and not self.losHead:
            self.changeFrames(self.losthead_attack_frames)
            self.setLostHead()
        elif self.health <= c.NORMAL_HEALTH and self.helmet:
            self.changeFrames(self.attack_frames)
            self.helmet = False
        if (self.current_time - self.attack_timer) > (c.ATTACK_INTERVAL * self.getTimeRatio()):
            if self.prey.health > 0:
                if self.prey_is_plant:
                    self.prey.setDamage(self.damage, self)
                else:
                    self.prey.setDamage(self.damage)
            self.attack_timer = self.current_time

        if self.prey.health <= 0:
            self.prey = None
            self.setWalk()
    
    def dying(self):
        pass

    def freezing(self):
        if self.health <= 0:
            self.setDie()
        elif self.health <= c.LOSTHEAD_HEALTH and not self.losHead:
            if self.old_state == c.WALK:
                self.changeFrames(self.losthead_walk_frames)
            else:
                self.changeFrames(self.losthead_attack_frames)
            self.setLostHead()
        if (self.current_time - self.freeze_timer) > c.FREEZE_TIME:
            # 解冻后回到被冻住之前的状态，否则正在啃植物的僵尸会掉头走人
            if self.old_state == c.ATTACK and self.prey is not None and self.prey.health > 0:
                self.setAttack(self.prey, self.prey_is_plant)
            else:
                self.prey = None
                self.setWalk()

    def setLostHead(self):
        self.losHead = True
        if self.head_group is not None:
            self.head_group.add(ZombieHead(self.rect.centerx, self.rect.bottom))

    def changeFrames(self, frames):
        '''change image frames and modify rect position'''
        self.frames = frames
        self.frame_num = len(self.frames)
        self.frame_index = 0
        
        bottom = self.rect.bottom
        centerx = self.rect.centerx
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.centerx = centerx

    def animation(self):
        if self.state == c.FREEZE:
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

        self.image = self.frames[self.frame_index]
        if self.is_hypno:
            self.image = pg.transform.flip(self.image, True, False)
        if(self.current_time - self.hit_timer) >= c.PLANT_HIT_FLASH_TIME:
            self.image.set_alpha(c.PLANT_ALPHA_NORMAL)
        else:
            self.image.set_alpha(c.PLANT_ALPHA_HIT)

    def getTimeRatio(self):
        return self.ice_slow_ratio

    def setIceSlow(self):
        '''when get a ice bullet damage, slow the attack or walk speed of the zombie'''
        self.ice_slow_timer = self.current_time
        self.ice_slow_ratio = 2

    def updateIceSlow(self):
        if self.ice_slow_ratio > 1:
            if (self.current_time - self.ice_slow_timer) > c.ICE_SLOW_TIME:
                self.ice_slow_ratio = 1

    def setDamage(self, damage, ice=False):
        self.health -= damage
        self.hit_timer = self.current_time
        if ice:
            self.setIceSlow()
    
    def setWalk(self):
        self.state = c.WALK
        self.animate_interval = c.ZOMBIE_ANIMATE_INTERVAL_WALK
        
        if self.helmet:
            self.changeFrames(self.helmet_walk_frames)
        elif self.losHead:
            self.changeFrames(self.losthead_walk_frames)
        else:
            self.changeFrames(self.walk_frames)

    def setAttack(self, prey, is_plant=True):
        self.prey = prey  # prey can be plant or other zombies
        self.prey_is_plant = is_plant
        self.state = c.ATTACK
        self.attack_timer = self.current_time
        self.animate_interval = c.ZOMBIE_ANIMATE_INTERVAL_ATTACK
        
        if self.helmet:
            self.changeFrames(self.helmet_attack_frames)
        elif self.losHead:
            self.changeFrames(self.losthead_attack_frames)
        else:
            self.changeFrames(self.attack_frames)
    
    def setDie(self):
        self.state = c.DIE
        self.animate_interval = c.ZOMBIE_ANIMATE_INTERVAL_DIE
        self.changeFrames(self.die_frames)
    
    def setBoomDie(self):
        self.state = c.DIE
        self.animate_interval = c.ZOMBIE_ANIMATE_INTERVAL_DIE
        self.changeFrames(self.boomdie_frames)

    def setFreeze(self, ice_trap_image):
        self.old_state = self.state
        self.state = c.FREEZE
        self.freeze_timer = self.current_time
        self.ice_trap_image = ice_trap_image
        self.ice_trap_rect = ice_trap_image.get_rect()
        self.ice_trap_rect.centerx = self.rect.centerx
        self.ice_trap_rect.bottom = self.rect.bottom

    def drawFreezeTrap(self, surface):
        if self.state == c.FREEZE:
            surface.blit(self.ice_trap_image, self.ice_trap_rect)

    def setHypno(self):
        self.is_hypno = True
        self.setWalk()


class ZombieHead(Zombie):
    """Zombie head that appears when zombie loses its head."""
    
    def __init__(self, x, y):
        Zombie.__init__(self, x, y, c.ZOMBIE_HEAD, 0)
        self.state = c.DIE
    
    def loadImages(self):
        self.die_frames = []
        die_name = self.name
        self.loadFrames(self.die_frames, die_name, 0)
        self.frames = self.die_frames

    def setWalk(self):
        self.animate_interval = c.ZOMBIE_ANIMATE_INTERVAL_ATTACK
