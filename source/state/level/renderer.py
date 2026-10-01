"""
Level rendering
"""
import pygame as pg
from ... import constants as c


class LevelRenderer:
    def __init__(self, level):
        self.level = level
    
    def drawMouseShow(self, surface):
        """Draw plant preview and mouse cursor"""
        if self.level.hint_plant:
            surface.blit(self.level.hint_image, self.level.hint_rect)
        x, y = pg.mouse.get_pos()
        self.level.mouse_rect.centerx = x
        self.level.mouse_rect.centery = y
        surface.blit(self.level.mouse_image, self.level.mouse_rect)

    def drawZombieFreezeTrap(self, i, surface):
        """Draw freeze trap effects on zombies"""
        for zombie in self.level.zombie_groups[i]:
            zombie.drawFreezeTrap(surface)

    def draw(self, surface):
        """Main draw method"""
        self.level.level.blit(self.level.background, self.level.viewport, self.level.viewport)
        surface.blit(self.level.level, (0, 0), self.level.viewport)
        
        if self.level.state == c.CHOOSE:
            self.level.panel.draw(surface)
        elif self.level.state == c.PLAY:
            self.level.menubar.draw(surface)
            
            # Draw all game entities
            for i in range(self.level.map_y_len):
                self.level.plant_groups[i].draw(surface)
                self.level.zombie_groups[i].draw(surface)
                self.level.hypno_zombie_groups[i].draw(surface)
                self.level.bullet_groups[i].draw(surface)
                self.drawZombieFreezeTrap(i, surface)
            
            # Draw cars, heads, and suns
            for car in self.level.cars:
                car.draw(surface)
            self.level.head_group.draw(surface)
            self.level.sun_group.draw(surface)

            # Draw mouse cursor if dragging plant or in shovel mode
            if self.level.drag_plant or self.level.shovel_mode:
                self.drawMouseShow(surface)
            
            # Draw pause menu if paused
            if self.level.paused:
                self.level.pause_menu.draw(surface)
