import cairo
import math
from Settings import *

enemy_data =[
    
    
    
]

class Enemy:
    def __init__(self,x,y, word, speed, radius):
        self.x = float(x)
        self.y = float(y)
        self.is_alive = True
        self.target_word = word.upper()
        self.speed = speed
        self.radius = radius
    
    def update(self, dt, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.hypot(dx, dy)
        
        if distance > 1:
            dx = dx / distance
            dy = dy / distance
        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt

        if distance < self.radius + 20:
            self.is_alive = False
            
    def draw(self,ctx):
        
        ctx.save()
        ctx.translate(self.x, self.y) 
        
        #MUSUH (AHMAT FAJARUDIN INI)
        ctx.set_source_rgb(*C_RED_ENEMY) 
        ctx.arc(0, 0, self.radius, 0, 2 * math.pi) 
        ctx.fill()
        
        ctx.restore()
        
    def speed_up(self):
        self.speed *= 1.5