"""Component module - contains all game components."""
__author__ = 'marble_xu'

from . import plants
from . import zombies

# For backward compatibility, expose modules with singular names
plant = plants
zombie = zombies

__all__ = ['plants', 'plant', 'zombies', 'zombie']
