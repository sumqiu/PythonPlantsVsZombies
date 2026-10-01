__author__ = 'marble_xu'

import pygame as pg
from ... import constants as c
from .constants import CARD_CONFIG


_sun_font = None
_sun_image_cache = {}  # sun_value -> rendered Surface


def getSunValueImage(sun_value):
    """Return a cached image displaying the sun value; rebuild only when value changes."""
    global _sun_font
    if sun_value in _sun_image_cache:
        return _sun_image_cache[sun_value]

    if _sun_font is None:
        _sun_font = pg.font.Font(None, 24)   # not SysFont: see pause_menu.setup_menu

    width = 32
    msg_image = _sun_font.render(str(sun_value), True, c.NAVYBLUE, c.LIGHTYELLOW)
    msg_rect = msg_image.get_rect()
    msg_w = msg_rect.width

    image = pg.Surface([width, 17])
    x = width - msg_w
    image.fill(c.LIGHTYELLOW)
    image.blit(msg_image, (x, 0), (0, 0, msg_rect.w, msg_rect.h))
    image.set_colorkey(c.BLACK)

    _sun_image_cache[sun_value] = image
    return image


def getCardPool(data):
    """Get card pool from level data"""
    card_pool = []
    for card in data:
        tmp = card['name']
        for i, cfg in enumerate(CARD_CONFIG):
            if cfg["plant"] == tmp:
                card_pool.append(i)
                break
    return card_pool
