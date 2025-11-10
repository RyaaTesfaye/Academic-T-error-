import cairo
import math
from Settings import *

class Player:
    def __init__(self):
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.health = max_health_player
        self.is_attacking = False
        self.attack_range = attack_range_player
    
    def update(self, dt):
        pass
    
    def draw(self,ctx):
        ctx.save()

        ctx.translate(self.x, self.y)

        #BADAN
        ctx.set_source_rgb(*C_ALMET_BLUE) 
        ctx.rectangle(-20, 0, 40, 30)  
        ctx.fill()

        #KEPALA
        ctx.set_source_rgb(*C_SKIN)
        ctx.arc(0, -15, 15, 0, 2 * math.pi) 
        ctx.fill()

        #LAPTOP
        ctx.set_source_rgb(*C_LAPTOP_GREY)
        ctx.rectangle(-15, 20, 30, 5) 
        ctx.fill()
        
        #AREAA
        ctx.set_source_rgba(*C_RANGE_PLAYER) 
        ctx.arc(0, 0, self.attack_range, 0, 2 * math.pi)
        ctx.fill()

        ctx.restore()
        
    def take_damage(self,amount):
        self.health -= amount
        if self.health <= 0:
            print("Game Over")
        