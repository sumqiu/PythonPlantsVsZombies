__author__ = 'marble_xu'

from ... import tool
from ... import constants as c
from .card import Card
from .utils import getSunValueImage
from .constants import (
    PANEL_Y_START, PANEL_X_START, PANEL_Y_INTERNAL, 
    PANEL_X_INTERNAL, CARD_LIST_NUM
)


class Panel:
    """Card selection panel shown before level starts"""
    
    def __init__(self, card_list, sun_value):
        self.loadImages(sun_value)
        self.selected_cards = []
        self.selected_num = 0
        self.setupCards(card_list)

    def loadFrame(self, name):
        """Load a frame image"""
        frame = tool.GFX[name]
        rect = frame.get_rect()
        frame_rect = (rect.x, rect.y, rect.w, rect.h)

        return tool.get_image(tool.GFX[name], *frame_rect, c.WHITE, 1)

    def loadImages(self, sun_value):
        """Load all panel images"""
        self.menu_image = self.loadFrame(c.MENUBAR_BACKGROUND)
        self.menu_rect = self.menu_image.get_rect()
        self.menu_rect.x = 0
        self.menu_rect.y = 0

        self.panel_image = self.loadFrame(c.PANEL_BACKGROUND)
        self.panel_rect = self.panel_image.get_rect()
        self.panel_rect.x = 0
        self.panel_rect.y = PANEL_Y_START

        self.value_image = getSunValueImage(sun_value)
        self.value_rect = self.value_image.get_rect()
        self.value_rect.x = 21
        self.value_rect.y = self.menu_rect.bottom - 21

        self.button_image = self.loadFrame(c.START_BUTTON)
        self.button_rect = self.button_image.get_rect()
        self.button_rect.x = 155
        self.button_rect.y = 547

    def setupCards(self, card_list):
        """Setup all available cards in the panel"""
        self.card_list = []
        # Create a mapping from name_index to card_list position
        self.name_index_to_position = {}
        
        x = PANEL_X_START - PANEL_X_INTERNAL
        y = PANEL_Y_START + 43 - PANEL_Y_INTERNAL
        for i, index in enumerate(card_list):
            if i % 8 == 0:
                x = PANEL_X_START - PANEL_X_INTERNAL
                y += PANEL_Y_INTERNAL
            x += PANEL_X_INTERNAL
            self.card_list.append(Card(x, y, index, 0.75))
            # Map name_index to position in card_list
            self.name_index_to_position[index] = i

    def checkCardClick(self, mouse_pos):
        """Handle card click - add or remove cards from selection"""
        delete_card = None
        for card in self.selected_cards:
            if delete_card:  # when delete a card, move right cards to left
                card.rect.x -= 55
            elif card.checkMouseClick(mouse_pos):
                self.deleteCard(card.name_index)
                delete_card = card

        if delete_card:
            self.selected_cards.remove(delete_card)
            self.selected_num -= 1

        if self.selected_num == CARD_LIST_NUM:
            return

        for card in self.card_list:
            if card.checkMouseClick(mouse_pos):
                if card.canSelect():
                    self.addCard(card)
                break

    def addCard(self, card):
        """Add a card to the selected cards"""
        card.setSelect(False)
        y = 8
        x = 78 + self.selected_num * 55
        self.selected_cards.append(Card(x, y, card.name_index))
        self.selected_num += 1

    def deleteCard(self, name_index):
        """Remove a card from the selected cards"""
        # Use the mapping to find the correct position in card_list
        position = self.name_index_to_position.get(name_index)
        if position is not None:
            self.card_list[position].setSelect(True)

    def checkStartButtonClick(self, mouse_pos):
        """Check if the start button was clicked"""
        if self.selected_num < CARD_LIST_NUM:
            return False

        x, y = mouse_pos
        if (x >= self.button_rect.x and x <= self.button_rect.right and
            y >= self.button_rect.y and y <= self.button_rect.bottom):
            return True
        return False

    def getSelectedCards(self):
        """Get the list of selected card indices"""
        card_index_list = []
        for card in self.selected_cards:
            card_index_list.append(card.name_index)
        return card_index_list

    def draw(self, surface):
        """Draw the panel and all cards"""
        self.menu_image.blit(self.value_image, self.value_rect)
        surface.blit(self.menu_image, self.menu_rect)
        surface.blit(self.panel_image, self.panel_rect)
        for card in self.card_list:
            card.draw(surface)
        for card in self.selected_cards:
            card.draw(surface)

        if self.selected_num == CARD_LIST_NUM:
            surface.blit(self.button_image, self.button_rect)
