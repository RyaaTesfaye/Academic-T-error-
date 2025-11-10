import cairo
import math
from Settings import *
from Enemy import *

class Laser:
    def __init__(self, start_x,start_y, target_enemy):
        self.x = start_x
        self.y = start_y
        self.target = target_enemy
        self.speed = laser_speed
        self.width = laser_width
        self.width_glow = laser_width_glow
        self.length = laser_length
        self.angle = 0
        self.is_alive = True
    
    def update(self, dt):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.hypot(dx,dy)
        
        self.angle = math.atan2(dy, dx)
        
        if distance < laser_hitbox:
            self.is_alive = False
            self.target.take_damage(laser_damage)
        else:
            self.x += (dx / distance) * self.speed * dt
            self.y += (dy/distance) * self.speed * dt
    
    def draw(self,ctx):
        ctx.save() 
        ctx.translate(self.x, self.y)
        ctx.rotate(self.angle) 
        
        # Glow
        ctx.set_source_rgba(*C_LASER_GLOW)
        ctx.rectangle(0, -self.width_glow / 2, self.length, self.width_glow)
        ctx.fill()
        
        # Core
        ctx.set_source_rgba(*C_LASER)
        ctx.rectangle(0, -self.width / 2, self.length, self.width)
        ctx.fill()
        
        ctx.restore()