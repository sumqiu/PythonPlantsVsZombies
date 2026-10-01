__author__ = 'marble_xu'

import pygame as pg
from ... import tool
from ... import constants as c
from .constants import CARD_CONFIG


class Card:
    """Represents a plant card that can be selected and placed"""
    
    def __init__(self, x, y, name_index, scale=0.78):
        cfg = CARD_CONFIG[name_index]
        self.loadFrame(cfg["card"], scale)
        self.rect = self.orig_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.name_index = name_index
        self.sun_cost = cfg["sun"]
        self.frozen_time = cfg["cd"]
        self.frozen_timer = -self.frozen_time
        self.refresh_timer = 0
        self.select = True
        self._last_render_key = None  # (in_cooldown, frozen_height_px, affordable)

    def loadFrame(self, name, scale):
        """Load and scale the card image"""
        frame = tool.GFX[name]
        rect = frame.get_rect()
        width, height = rect.w, rect.h

        self.orig_image = tool.get_image(frame, 0, 0, width, height, c.BLACK, scale)
        self.image = self.orig_image

    def checkMouseClick(self, mouse_pos):
        """Check if the mouse click is on this card"""
        x, y = mouse_pos
        if (x >= self.rect.x and x <= self.rect.right and
            y >= self.rect.y and y <= self.rect.bottom):
            return True
        return False

    def canClick(self, sun_value, current_time):
        """Check if the card can be clicked (enough sun and not cooling down)"""
        if self.sun_cost <= sun_value and (current_time - self.frozen_timer) > self.frozen_time:
            return True
        return False

    def canSelect(self):
        """Check if the card can be selected"""
        return self.select

    def setSelect(self, can_select):
        """Set the card's selectable state"""
        self.select = can_select
        if can_select:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(128)

    def setFrozenTime(self, current_time):
        """Set the frozen timer to start cooldown"""
        self.frozen_timer = current_time

    def createShowImage(self, sun_value, current_time):
        """Create a card image to show cool down status or disable status"""
        time = current_time - self.frozen_timer
        if time < self.frozen_time:  # cool down status
            image = pg.Surface([self.rect.w, self.rect.h])
            frozen_image = self.orig_image.copy()
            frozen_image.set_alpha(128)
            frozen_height = (self.frozen_time - time) / self.frozen_time * self.rect.h
            
            image.blit(frozen_image, (0, 0), (0, 0, self.rect.w, frozen_height))
            image.blit(self.orig_image, (0, frozen_height),
                      (0, frozen_height, self.rect.w, self.rect.h - frozen_height))
        elif self.sun_cost > sun_value:  # disable status
            image = self.orig_image.copy()
            image.set_alpha(192)
        else:
            image = self.orig_image
        return image

    def update(self, sun_value, current_time):
        """Update the card's display state; rebuild image only when visual state changes."""
        if (current_time - self.refresh_timer) < 250:
            return
        self.refresh_timer = current_time

        time_elapsed = current_time - self.frozen_timer
        in_cooldown = time_elapsed < self.frozen_time
        affordable = self.sun_cost <= sun_value

        if in_cooldown:
            frozen_height = int((self.frozen_time - time_elapsed) / self.frozen_time * self.rect.h)
            render_key = (True, frozen_height, affordable)
        else:
            render_key = (False, 0, affordable)

        if render_key != self._last_render_key:
            self.image = self.createShowImage(sun_value, current_time)
            self._last_render_key = render_key

    def draw(self, surface):
        """Draw the card on the surface"""
        surface.blit(self.image, self.rect)
