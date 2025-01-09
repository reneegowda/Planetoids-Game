"""
The primary application script for Alien Invaders

This is the module with the application code.
"""

from consts import *
from app import *

# Application code
if __name__ == '__main__':
    Planetoids(width=GAME_WIDTH,height=GAME_HEIGHT).run()
