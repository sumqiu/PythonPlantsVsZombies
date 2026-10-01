"""
Shovel component for removing plants
"""
import pygame as pg
from ... import tool
from ... import constants as c


class Shovel:
    """Shovel tool for removing planted plants"""
    
    def __init__(self, x, y):
        self.loadFrame()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_active = False  # Whether shovel is currently selected
        
    def loadFrame(self):
        """Load the shovel image"""
        # Placeholder: will load actual shovel image when available
        # Expected image: resources/graphics/Screen/Shovel.png
        try:
            frame = tool.GFX[c.SHOVEL]
            self.image = frame
        except KeyError:
            # Create placeholder if image not found
            self.image = pg.Surface((50, 50))
            self.image.fill(c.GOLD)
            font = pg.font.Font(None, 18)      # not SysFont: see pause_menu.setup_menu
            text = font.render('SHOVEL', True, c.BLACK)
            text_rect = text.get_rect(center=(25, 25))
            self.image.blit(text, text_rect)
    
    def update(self, mouse_pos):
        """Update shovel state based on mouse position"""
        pass
    
    def checkMouseClick(self, mouse_pos):
        """Check if shovel was clicked"""
        x, y = mouse_pos
        if (x >= self.rect.x and x <= self.rect.right and
            y >= self.rect.y and y <= self.rect.bottom):
            return True
        return False
    
    def setActive(self, active):
        """Set shovel active/inactive state"""
        self.is_active = active
    
    def draw(self, surface):
        """Draw the shovel"""
        surface.blit(self.image, self.rect)
        
        # Draw highlight when active
        if self.is_active:
            pg.draw.rect(surface, c.GOLD, self.rect, 3)
