import cairo
import math
import random
import pygame
from Settings import *


class Player:
    def __init__(self):
        self.x = screen_width // 2 
        self.y = screen_height // 2 + 60
        self.health = max_health_player
        self.is_attacking = False
        self.attack_range = attack_range_player
        
        self.is_glitching = False
        self.glitch_timer = random.uniform(glitch_interval/2, glitch_interval)
        self.glitch_duration_timer = 0
        
        try:
            self.sprite_img = pygame.image.load("aditz3.png").convert_alpha()
            
            self.sprite_cairo = cairo.ImageSurface.create_for_data(
            self.sprite_img.get_buffer(),
            cairo.FORMAT_ARGB32,
            self.sprite_img.get_width(),
            self.sprite_img.get_height()
            )
        except:
            self.sprite_img = None
            
    def update(self, dt):
        if not glitch_enabled or not self.sprite_cairo:
            return
        if self.is_glitching:
            self.glitch_duration_timer += dt
            if self.glitch_duration_timer > glitch_duration:
                self.is_glitching = False
                self.glitch_duration_timer = 0
                self.glitch_timer = random.uniform(glitch_interval / 2, glitch_interval)
        else:
            self.glitch_timer -= dt
            if self.glitch_timer <= 0:
                self.is_glitching = True
    
    def draw(self,ctx):
        ctx.save()

        ctx.translate(self.x, self.y)
        
        #AREAA
        ctx.set_source_rgba(*C_RANGE_PLAYER) 
        ctx.arc(0, 0, self.attack_range, 0, 2 * math.pi)
        ctx.fill()
        
        #GLITCHHHH
        if self.is_glitching and self.sprite_cairo:
            sprite_width = 128
            sprite_height = 128
            spawn_x = -sprite_width / 2
            spawn_y = -(sprite_height / 2) + 20
            
            spawn_x += random.randint(-3,3)
            spawn_y += random.randint(-3,3)
            
            ctx.set_source_surface(self.sprite_cairo, spawn_x, spawn_y)
            ctx.paint_with_alpha(glitch_alpha)
        else:
            
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
            

        ctx.restore()
        
    def take_damage(self,amount):
        self.health -= amount
        if self.health <= 0:
            print("Game Over")
        