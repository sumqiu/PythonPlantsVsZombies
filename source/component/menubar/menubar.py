__author__ = 'marble_xu'

import pygame as pg
from ... import tool
from ... import constants as c
from .card import Card
from .utils import getSunValueImage
from .constants import CARD_CONFIG


class MenuBar:
    """Main menu bar during gameplay that displays cards and sun value"""
    
    def __init__(self, card_list, sun_value):
        self.loadFrame(c.MENUBAR_BACKGROUND)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 0
        
        self.sun_value = sun_value
        self.card_offset_x = 32
        # checkCardClick 会在第一帧 update() 之前读它，必须先存在
        self.current_time = 0
        self.setupCards(card_list)
        self.setupShovel()

    def setupShovel(self):
        """Setup the shovel tool"""
        from .shovel import Shovel
        # Position shovel at bottom right of menubar, below the cards
        shovel_x = self.rect.x + 600
        shovel_y = self.rect.y + 30
        self.shovel = Shovel(shovel_x, shovel_y)

    def loadFrame(self, name):
        """Load the menu bar background image"""
        frame = tool.GFX[name]
        rect = frame.get_rect()
        frame_rect = (rect.x, rect.y, rect.w, rect.h)

        self.image = tool.get_image(tool.GFX[name], *frame_rect, c.WHITE, 1)

    def update(self, current_time):
        """Update all cards in the menu bar"""
        self.current_time = current_time
        for card in self.card_list:
            card.update(self.sun_value, self.current_time)
        self.shovel.update(None)

    def createImage(self, x, y, num):
        """Create extended menu bar image for multiple sections"""
        if num == 1:
            return
        img = self.image
        rect = self.image.get_rect()
        width = rect.w
        height = rect.h
        self.image = pg.Surface((width * num, height)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        for i in range(num):
            x = i * width
            self.image.blit(img, (x, 0))
        self.image.set_colorkey(c.BLACK)
    
    def setupCards(self, card_list):
        """Setup cards in the menu bar"""
        self.card_list = []
        x = self.card_offset_x
        y = 8
        for index in card_list:
            x += 55
            self.card_list.append(Card(x, y, index))

    def checkCardClick(self, mouse_pos):
        """Check if a card was clicked and return plant name and card"""
        result = None
        for card in self.card_list:
            if card.checkMouseClick(mouse_pos):
                if card.canClick(self.sun_value, self.current_time):
                    result = (CARD_CONFIG[card.name_index]["plant"], card)
                break
        return result
    
    def checkShovelClick(self, mouse_pos):
        """Check if shovel was clicked"""
        return self.shovel.checkMouseClick(mouse_pos)
    
    def setShovelActive(self, active):
        """Set shovel active/inactive state"""
        self.shovel.setActive(active)
    
    def isShovelActive(self):
        """Check if shovel is currently active"""
        return self.shovel.is_active
    
    def checkMenuBarClick(self, mouse_pos):
        """Check if the menu bar was clicked"""
        x, y = mouse_pos
        if (x >= self.rect.x and x <= self.rect.right and
            y >= self.rect.y and y <= self.rect.bottom):
            return True
        return False

    def decreaseSunValue(self, value):
        """Decrease the sun value"""
        self.sun_value -= value

    def increaseSunValue(self, value):
        """Increase the sun value"""
        self.sun_value += value

    def setCardFrozenTime(self, plant_name):
        """Set the frozen time for a specific plant card"""
        for card in self.card_list:
            if CARD_CONFIG[card.name_index]["plant"] == plant_name:
                card.setFrozenTime(self.current_time)
                break

    def drawSunValue(self):
        """Draw the sun value on the menu bar"""
        self.value_image = getSunValueImage(self.sun_value)
        self.value_rect = self.value_image.get_rect()
        self.value_rect.x = 21
        self.value_rect.y = self.rect.bottom - 21
        
        self.image.blit(self.value_image, self.value_rect)

    def draw(self, surface):
        """Draw the menu bar and all cards"""
        self.drawSunValue()
        surface.blit(self.image, self.rect)
        for card in self.card_list:
            card.draw(surface)
        self.shovel.draw(surface)
