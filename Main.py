import pygame
import cairo
import math
from Settings import *
from Player import *
from Enemy import *
from Particle import *

pygame.init()

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Akademia T(error)")

surface_cairo = pygame.Surface((screen_width,screen_height), pygame.SRCALPHA)

#OBJEK DISINI
player_satu = Player()



#Game Loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill((255,255,255))
    
    surface_bridge = cairo.ImageSurface.create_for_data(
    surface_cairo.get_buffer(),
    cairo.FORMAT_ARGB32,
    screen_width,
    screen_height
)
    ctx = cairo.Context(surface_bridge)
    
    surface_cairo.fill((0,0,0,0))
    #GAMBAR BG DISINI
  
    
    
    #GAMBAR OBJEK DISINI
    player_satu.draw(ctx)
    
    
    
    # -----------------------
    surface_bridge.flush()
    del ctx
    del surface_bridge
    
    screen.blit(surface_cairo, (0, 0))
    pygame.display.flip()
    
    clock.tick(fps)
    
pygame.quit()