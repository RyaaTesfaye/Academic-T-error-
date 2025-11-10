import cairo
import math
from Settings import *

class Player:
    def __init__(self):
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.health = max_health_player
    
    def update(self):
        pass
    
    def draw(self,ctx):
        pass