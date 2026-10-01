"""Zombie components for the game."""

__author__ = 'marble_xu'

from .base import Zombie, ZombieHead
from .normal import NormalZombie, FlagZombie
from .armored import ConeHeadZombie, BucketHeadZombie
from .special import NewspaperZombie
from .playable import PlayableBucketHeadZombie, PlayableConeHeadZombie, PlayableNormalZombie

__all__ = [
    'Zombie',
    'ZombieHead',
    'NormalZombie',
    'FlagZombie',
    'ConeHeadZombie',
    'BucketHeadZombie',
    'NewspaperZombie',
    'PlayableBucketHeadZombie',
    'PlayableConeHeadZombie',
    'PlayableNormalZombie',
]
