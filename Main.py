import pygame
import cairo
import math
import random
from Settings import *
from Player import *
from Enemy import *
from Particle import *
from background import *

pygame.init()

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Akademia T(error)")

surface_cairo = pygame.Surface((screen_width,screen_height), pygame.SRCALPHA)

#OBJEK DISINI
player_satu = Player()
background = Background()
enemy_list = []
partikel_list = []




#------------------
target_enemy = None
current_type_word = ""
last_spawn_time = 0


#Game Loop
running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(fps) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if target_enemy:
                if event.unicode.isalpha():
                    pressed_letter = event.unicode.upper()
                    target_word = target_enemy.target_word.upper()
                    current_index = len(current_type_word)
                    
                    if current_index < len(target_word) and pressed_letter == target_word[current_index]:
                        current_type_word += pressed_letter
                        
                        new_laser = Laser(player_satu.x, player_satu.y,target_enemy )
                        partikel_list.append(new_laser)
                        
                        if len(current_type_word) == len(target_word):
                            target_enemy.is_alive = False
                            
                            end_pos = (target_enemy.x, target_enemy.y)
                            new_bomb = Bomb(player_satu.x, player_satu.y,end_pos)
                            partikel_list.append(new_bomb)
                            
                            target_enemy = None
                            current_type_word = ""
                    else:
                        current_type_word = ""
                        target_enemy.speed_up()
                    
            
    #UPDATEEEE PLAYER      
    player_satu.update(dt)
    
    #SPAWNER ENEMY
    current_time = pygame.time.get_ticks() / 1000
    
    if current_time - last_spawn_time > interval_spawn:
        
        tipe = random.choice(['gampang','sedang','elite','susah','boss'])
        
        side = random.choice(['atas', 'bawah', 'kanan','kiri'])
        spawn_padding = 20
        
        if side == 'atas':
            spawn_x = random.randint(0, screen_width)
            spawn_y = -spawn_padding
        elif side == 'bawah':
            spawn_x = random.randint(0, screen_width)
            spawn_y = screen_height + spawn_padding
        elif side == 'kanan':
            spawn_x = screen_width + spawn_padding
            spawn_y = random.randint(0,screen_height)
        elif side == 'kiri':
            spawn_x = -spawn_padding
            spawn_y = random.randint(0,screen_height)
        
        new_enemy = Enemy(spawn_x, spawn_y, tipe)
        enemy_list.append(new_enemy)
        
        last_spawn_time = current_time
    
    for enemy in enemy_list:
        enemy.update(dt,player_satu.x, player_satu.y)     
            
    # CEK TARGET
    if  target_enemy:
        if not target_enemy.is_alive:
            target_enemy = None
            current_type_word = ""
    
    if not target_enemy:
        closest_enemy = None
        min_distance = float('inf')
        
        for enemy in enemy_list:
            distance = math.hypot(player_satu.x - enemy.x, player_satu.y - enemy.y)
            
            if distance <= player_satu.attack_range:
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
                    
        if closest_enemy:
            target_enemy = closest_enemy
            current_type_word = ""
            
        
    if target_enemy and not target_enemy.is_alive:
        target_enemy = None        
    #UPDATE PARTIKEL
    
    for partikel in partikel_list:
        partikel.update(dt)
    #---------------------------------
   
            
    # --------------------------------
    surface_bridge = cairo.ImageSurface.create_for_data(
    surface_cairo.get_buffer(),
    cairo.FORMAT_ARGB32,
    screen_width,
    screen_height
)
    ctx = cairo.Context(surface_bridge)
    surface_cairo.fill((0,0,0,0))
    # ----------------------------------
    
    #GAMBAR BG DISINI
    # ctx.set_source_rgb(*C_WHITE)
    # ctx.paint()
    background.draw(ctx)
      
    
    #GAMBAR OBJEK DISINI
    player_satu.draw(ctx)

    
    for enemy in enemy_list:
        enemy.draw(ctx)
        
        #--------------------
        if enemy == target_enemy:  
            
            #Sorotan
            ctx.save()
            ctx.translate(enemy.x, enemy.y)
            ctx.set_source_rgba(*C_SOROTAN) 
            ctx.set_line_width(3)
            ctx.arc(0, 0, enemy.radius  + 5, 0, 2 * math.pi) 
            ctx.stroke()
            ctx.restore()
            
            #Kata kata
            word_to_draw = enemy.target_word.upper()
            typed_part = ""
            
            if enemy == target_enemy:
                typed_part = current_type_word
                
            untyped_part = word_to_draw[len(typed_part):]
            
            #font
            ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            ctx.set_font_size(16)
                
            # POSISI TEKS
            (x_bearing, y_bearing, text_width, text_height, x_advance, y_advance) = ctx.text_extents(word_to_draw)
            text_x_pos = enemy.x - (text_width / 2)
            text_y_pos = enemy.y - 30
            
            # #sudah diketik
            # ctx.set_source_rgb(*C_GREEN)
            # ctx.move_to(text_x_pos, text_y_pos)
            # ctx.show_text(typed_part)
            
            #sisanya
            ctx.set_source_rgb(*C_BLACK)
            ctx.move_to(text_x_pos, text_y_pos)
            ctx.show_text(" " * len(typed_part) + untyped_part)
            #--------------------------------------
        
    
    for partikel in partikel_list:
        partikel.draw(ctx)


    #TIMEEEEEEEEEEEEEEEEEEEEEER
    timer_text = f"Waktu: {current_time:.2f}" 
    
    ctx.set_source_rgb(*C_BLACK) 
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(24)
    
    (x_bearing, y_bearing, text_width, text_height, x_advance, y_advance) = ctx.text_extents(timer_text)
    
    text_x_pos = (screen_width / 2) - (text_width / 2)
    text_y_pos = 40 
    
    ctx.move_to(text_x_pos, text_y_pos)
    ctx.show_text(timer_text)

    # -----------------------
    surface_bridge.flush()
    del ctx
    del surface_bridge
    screen.blit(surface_cairo, (0, 0))
    pygame.display.flip()
    #------------------------
    
    enemy_list = [e for e in enemy_list if e.is_alive]
    partikel_list = [p for p in partikel_list if p.is_alive]
    
    clock.tick(fps)
    
pygame.quit()