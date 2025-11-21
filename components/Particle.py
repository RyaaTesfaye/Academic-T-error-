import cairo
import math
from Settings import *
from enemy.Enemy import Enemy

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
        
class Bomb:
    def __init__(self, start_x, start_y, end_pos):
        self.x = start_x
        self.y = start_y
        self.end_x, self.end_y = end_pos
        
        self.control_x = (self.x + self.end_x) / 2
        self.control_y = (self.y + self.end_y) / 2 + 100
        
        self.lifespan = 0.2
        self.is_alive = True
    
    def update(self, dt):
        self.lifespan -= dt
        if self.lifespan <= 0:
            self.is_alive = False
    
    def draw(self, ctx):
        ctx.save()
        
        ctx.set_source_rgba(*C_BOMB_GLOW) 
        ctx.set_line_width(8) 
        
        ctx.move_to(self.x, self.y) 
        ctx.curve_to(self.control_x, self.control_y, 
                     self.control_x, self.control_y, 
                     self.end_x, self.end_y)
        ctx.stroke() 
        
        ctx.set_source_rgb(*C_BOMB) 
        ctx.set_line_width(3) 
        
        ctx.move_to(self.x, self.y)
        ctx.curve_to(self.control_x, self.control_y, 
                     self.control_x, self.control_y, 
                     self.end_x, self.end_y)
        ctx.stroke()
        
        ctx.restore()