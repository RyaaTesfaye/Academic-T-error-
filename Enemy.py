import cairo
import math
from Settings import *

class Enemy:
    def __init__(self,x,y, word, speed, radius):
        self.x = float(x)
        self.y = float(y)
        self.is_alive = True
        self.target_word = word
        self.speed = speed
        self.radius = radius
        self.health = 100
    
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
        
        # KATA KATA
        ctx.set_source_rgb(*C_BLACK)
        ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(16)
        
        # POSISI TEKS
        (x_bearing, y_bearing, text_width, text_height, x_advance, y_advance) = ctx.text_extents(self.target_word)
        text_x_pos = -text_width / 2
        text_y_pos = -self.radius - 10 
        
        ctx.move_to(text_x_pos, text_y_pos)
        ctx.show_text(self.target_word)
        
        ctx.restore()
    
    def take_damage(self, amount):
        self.health -= amount
        
        if self.health <= 0:
            self.health = 100
            # self.is_alive = False
        
    def speed_up(self):
        self.speed *= 1.5