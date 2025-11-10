import cairo
import math
from Settings import *

class Enemy:
    def __init__(self,x,y):
        self.x = float(x)
        self.y = float(y)
        self.is_alive = True
        self.target_word = "Ahmat"
    
    def update(self, dt, player_x, player_y):
        pass
    
    def draw(self,ctx):
        ctx.set_source_rgb(*C_RED_ENEMY)
        ctx.arc(self.x, self.y, 10, 0, 2 * math.pi) 
        ctx.fill()
    
    def take_damage(self, amount):
        self.is_alive = False
        
    def speed_up():
        pass