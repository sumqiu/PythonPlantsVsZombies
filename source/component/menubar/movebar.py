__author__ = 'marble_xu'

import random
import pygame as pg
from ... import tool
from ... import constants as c
from .constants import CARD_CONFIG


class MoveCard:
    """A card that moves from right to left in the move bar"""
    
    def __init__(self, x, y, card_name, plant_name, scale=0.78):
        self.loadFrame(card_name, scale)
        self.rect = self.orig_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.w = 1
        self.image = self.createShowImage()

        self.card_name = card_name
        self.plant_name = plant_name
        self.move_timer = 0
        self.select = True

    def loadFrame(self, name, scale):
        """Load and scale the card image"""
        frame = tool.GFX[name]
        rect = frame.get_rect()
        width, height = rect.w, rect.h

        self.orig_image = tool.get_image(frame, 0, 0, width, height, c.BLACK, scale)
        self.orig_rect = self.orig_image.get_rect()
        self.image = self.orig_image

    def checkMouseClick(self, mouse_pos):
        """Check if the mouse click is on this card"""
        x, y = mouse_pos
        if (x >= self.rect.x and x <= self.rect.right and
            y >= self.rect.y and y <= self.rect.bottom):
            return True
        return False

    def createShowImage(self):
        """Create a part card image when card appears from left"""
        if self.rect.w < self.orig_rect.w:  # create a part card image
            image = pg.Surface([self.rect.w, self.rect.h])
            image.blit(self.orig_image, (0, 0), (0, 0, self.rect.w, self.rect.h))
            self.rect.w += 1
        else:
            image = self.orig_image
        return image

    def update(self, left_x, current_time):
        """Update card position and appearance"""
        if self.move_timer == 0:
            self.move_timer = current_time
        elif (current_time - self.move_timer) >= c.CARD_MOVE_TIME:
            if self.rect.x > left_x:
                self.rect.x -= 1
                self.image = self.createShowImage()
            self.move_timer += c.CARD_MOVE_TIME

    def draw(self, surface):
        """Draw the card on the surface"""
        surface.blit(self.image, self.rect)


class MoveBar:
    """Conveyor belt bar that continuously provides random cards"""
    
    def __init__(self, card_pool):
        self.loadFrame(c.MOVEBAR_BACKGROUND)
        self.rect = self.image.get_rect()
        self.rect.x = 90
        self.rect.y = 0
        
        self.card_start_x = self.rect.x + 8
        self.card_end_x = self.rect.right - 5
        self.card_pool = card_pool
        self.card_list = []
        self.create_timer = -c.MOVEBAR_CARD_FRESH_TIME

    def loadFrame(self, name):
        """Load the move bar background image"""
        frame = tool.GFX[name]
        rect = frame.get_rect()
        frame_rect = (rect.x, rect.y, rect.w, rect.h)

        self.image = tool.get_image(tool.GFX[name], *frame_rect, c.WHITE, 1)

    def createCard(self):
        """Create a new card at the right end of the bar"""
        if len(self.card_list) > 0 and self.card_list[-1].rect.right > self.card_end_x:
            return False
        x = self.card_end_x
        y = 6
        index = random.randint(0, len(self.card_pool) - 1)
        card_index = self.card_pool[index]
        cfg = CARD_CONFIG[card_index]
        card_name = cfg["card"] + '_move'
        plant_name = cfg["plant"]
        self.card_list.append(MoveCard(x, y, card_name, plant_name))
        return True

    def update(self, current_time):
        """Update all cards and create new ones"""
        self.current_time = current_time
        left_x = self.card_start_x
        for card in self.card_list:
            card.update(left_x, self.current_time)
            left_x = card.rect.right + 1

        if (self.current_time - self.create_timer) > c.MOVEBAR_CARD_FRESH_TIME:
            if self.createCard():
                self.create_timer = self.current_time

    def checkCardClick(self, mouse_pos):
        """Check if a card was clicked and return plant name and card"""
        result = None
        for index, card in enumerate(self.card_list):
            if card.checkMouseClick(mouse_pos):
                result = (card.plant_name, card)
                break
        return result
    
    def checkMenuBarClick(self, mouse_pos):
        """Check if the move bar was clicked"""
        x, y = mouse_pos
        if (x >= self.rect.x and x <= self.rect.right and
            y >= self.rect.y and y <= self.rect.bottom):
            return True
        return False

    def deleteCard(self, card):
        """Remove a card from the move bar"""
        self.card_list.remove(card)

    def draw(self, surface):
        """Draw the move bar and all cards"""
        surface.blit(self.image, self.rect)
        for card in self.card_list:
            card.draw(surface)
