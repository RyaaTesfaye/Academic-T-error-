import pygame
import cairo
import math
import random
from Settings import *
from Player import *
from enemy.Enemy import Enemy
from components.Particle import *
from background import *
from wave_manager import *
from score.score import highscore, listScore
from sound_manager import SoundManager
from ui import UI 

# ============================================
# INISIALISASI PYGAME
# ============================================
pygame.init()
pygame.mixer.init()

# SETUP DISPLAY WINDOW
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Academia T(error)")

# ============================================
# SETUP CAIRO SURFACE
# ============================================
surface_cairo = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

# ============================================
# INISIALISASI OBJEK GAME
# ============================================
player_satu = Player()
background = Background()
wave_manager = wave_managers()
ui_manager = UI() 

enemy_list = []
partikel_list = []
current_time = 0
target_enemy = None
current_type_word = ""

# ============================================
# SETUP AUDIO
# ============================================
sound_manager = SoundManager()
sound_manager.play_bgm()

# ============================================
# VARIABEL GAME STATE
# ============================================
game_state = "MENU"
last_skor_time = 0
Menu = True
Main = True
start_time = 0
paused = False

# Variabel UI Scoreboard
scoreList = {}
arrow_x, arrow_y = 1070, 60
Is_Full = True
click_cooldown = 0.3
last_click_time = 0

# ============================================
# GAME LOOP UTAMA
# ============================================
running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(fps) / 1000.0
    current_time = pygame.time.get_ticks() / 1000

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # SETUP CAIRO
    surface_bridge = cairo.ImageSurface.create_for_data(
        surface_cairo.get_buffer(), cairo.FORMAT_ARGB32, screen_width, screen_height
    )
    ctx = cairo.Context(surface_bridge)
    surface_cairo.fill((0, 0, 0, 0))

    # ============================================
    # STATE: PLAY
    # ============================================
    if game_state == "PLAY":
        if Main:
            liveScore = listScore()
            Main = False
            game_time = 0

        # INPUT KETIKAN
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if paused: 
                        sound_manager.pause_bgm()
                    else: 
                        sound_manager.unpause_bgm()
                    continue  
                
                if not paused:
                    
                    # DEBUG
                    # if event.key == pygame.K_v: 
                    #     wave_manager.is_game_cleared = True
                    #     enemy_list = []
                    # if event.key == pygame.K_q: 
                    #     player_satu.health = 0
                    # if event.key == pygame.K_b:
                    #     background.next_background()


                    # mekanik ngetik buat nembak musuh
                    if target_enemy:
                        if event.unicode.isalpha():
                            pressed_letter = event.unicode.upper()
                            target_word = target_enemy.target_word.upper()
                            current_index = len(current_type_word)

                            if current_index < len(target_word) and pressed_letter == target_word[current_index]:
                                current_type_word += pressed_letter
                                sound_manager.play_sfx("laser")
                                partikel_list.append(Laser(player_satu.x, player_satu.y, target_enemy))

                                if len(current_type_word) == len(target_word):
                                    target_enemy.is_alive = False
                                    sound_manager.play_sfx("bomb")
                                    partikel_list.append(Bomb(player_satu.x, player_satu.y, (target_enemy.x, target_enemy.y)))
                                    target_enemy = None; current_type_word = ""
                            else:
                                current_type_word = ""; target_enemy.speed_up()
            
            elif event.type == pygame.MOUSEBUTTONDOWN and not paused:
                mouse_pos = event.pos
                arrow_hitbox = pygame.Rect(0, 0, 30, 30)
                arrow_hitbox.center = (arrow_x, arrow_y)
                if arrow_hitbox.collidepoint(mouse_pos):
                    if current_time - last_click_time > click_cooldown:
                        Is_Full = not Is_Full
                        last_click_time = current_time
                        arrow_y = 60 if Is_Full else 217

        # UPDATE LOGIC GAME
        if not paused:
            game_time = (pygame.time.get_ticks() / 1000) - start_time
            player_satu.update(dt, sound_manager.sfx)
            
            if player_satu.health <= 0:
                game_state = "GAMEOVER"
                sound_manager.stop_bgm()

            if wave_manager.is_game_cleared and len(enemy_list) == 0:
                game_state = "VICTORY"

            last_skor_time = game_time

            # spawn musuh per wave
            spawn_result = wave_manager.update(dt, len(enemy_list))
            if spawn_result == "WAVE_CLEARED":
                game_state = "LEVEL_UP"
            elif spawn_result:
                side = random.choice(['atas', 'bawah', 'kanan', 'kiri'])
                spawn_padding = 20
                if side == 'atas': sx, sy = random.randint(0, screen_width), -spawn_padding
                elif side == 'bawah': sx, sy = random.randint(0, screen_width), screen_height + spawn_padding
                elif side == 'kanan': sx, sy = screen_width + spawn_padding, random.randint(0, screen_height)
                elif side == 'kiri': sx, sy = -spawn_padding, random.randint(0, screen_height)
                enemy_list.append(Enemy(sx, sy, spawn_result))

            for enemy in enemy_list: enemy.update(dt, player_satu)

            # targeting musuh terdekat
            if target_enemy and not target_enemy.is_alive:
                target_enemy = None; current_type_word = ""
            if not target_enemy:
                closest, min_dist = None, float('inf')
                for enemy in enemy_list:
                    dist = math.hypot(player_satu.x - enemy.x, player_satu.y - enemy.y)
                    if dist <= player_satu.attack_range and dist < min_dist:
                        min_dist = dist; closest = enemy
                if closest: target_enemy = closest; current_type_word = ""
            
            for p in partikel_list: 
                p.update(dt)
            
            if not Main: 
                liveScore["you"] = float(f"{game_time:.2f}")

        # RENDER
        background.draw(screen)
        player_satu.draw(ctx)

        for enemy in enemy_list:
            enemy.draw(ctx)
            if enemy == target_enemy:
                # highlight target sama tampilin kata
                ctx.save(); ctx.translate(enemy.x, enemy.y)
                ctx.set_source_rgba(*C_SOROTAN); ctx.set_line_width(3)
                ctx.arc(0, 0, enemy.radius + 5, 0, 2 * math.pi); ctx.stroke(); ctx.restore()
                
                word = enemy.target_word.upper(); typed = current_type_word
                untyped = word[len(typed):]
                
                ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(16)
                (xb, yb, w, h, xa, ya) = ctx.text_extents(word)
                tx, ty = enemy.x - (w / 2), enemy.y - 30
                ctx.set_source_rgb(*C_BLACK); ctx.move_to(tx, ty); ctx.show_text(" " * len(typed) + untyped)

        for p in partikel_list:
            p.draw(ctx)

        ui_manager.draw_hud(ctx, player_satu, wave_manager, screen_height, screen_width)
        
        if not Main:
            ui_manager.draw_scoreboard_overlay(ctx, liveScore, Is_Full, arrow_x, arrow_y)
            
        if paused:
            ui_manager.draw_pause(ctx, screen_width, screen_height)

    # ============================================
    # STATE: MENU
    # ============================================
    elif game_state == "MENU":
        tombol_rect = pygame.Rect((screen_width / 2) - 100, (screen_height / 2) +150, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        tombol_hover = tombol_rect.collidepoint(mouse_pos)

        for event in events:
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    sound_manager.next_bgm()
                elif event.key == pygame.K_LEFT:
                    sound_manager.prev_bgm()
            
            # klik tombol mulai game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tombol_hover:
                    game_state = "PLAY"
                    sound_manager.play_bgm(loops=-1)
                    # reset semua variabel
                    player_satu = Player()
                    enemy_list = []
                    partikel_list = []
                    current_type_word = ""; 
                    target_enemy = None
                    score_calculated = False
                    paused = False
                    wave_manager = wave_managers()
                    start_time = pygame.time.get_ticks() / 1000

        background.draw(screen)
        if Menu:
            scoreList = listScore(); Menu = False
            
        current_song_name = sound_manager.get_current_bgm_name()
        ui_manager.draw_menu(ctx, screen_width, screen_height, scoreList, tombol_rect, tombol_hover, current_song_name)
            

    # ============================================
    # STATE: GAMEOVER
    # ============================================    
    elif game_state == "GAMEOVER":
        if not score_calculated:
            timer_end = highscore(last_skor_time)
            Menu = True
            Main = True
            score_calculated = True
            sound_manager.stop_bgm()
            sound_manager.play_sfx("game_over")

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "MENU"
        
        background.draw(screen)
        ui_manager.draw_game_over(ctx, screen_width, screen_height, timer_end, scoreList.get("you", 0))

    # ============================================
    # STATE: VICTORY
    # ============================================
    elif game_state == "VICTORY":
        if pygame.mixer.music.get_busy(): 
            sound_manager.stop_bgm()
        if not score_calculated:
            timer_end = highscore(last_skor_time)
            Menu = True
            Main = True
            score_calculated = True
            sound_manager.play_sfx("victory")

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "MENU"

        background.draw(screen)
        ui_manager.draw_victory(ctx, screen_width, screen_height, last_skor_time, scoreList.get("you", 0))

    # ============================================
    # STATE: LEVEL UP
    # ============================================
    elif game_state == "LEVEL_UP":
        # pilih upgrade pake angka 1,2,3
        for event in events:
            if event.type == pygame.KEYDOWN:
                upgrade_chosen = False
                if event.key == pygame.K_1:
                    player_satu.health = min(player_satu.health + 1, max_health_player)
                    upgrade_chosen = True
                elif event.key == pygame.K_2:
                    player_satu.attack_range += 10
                    upgrade_chosen = True
                elif event.key == pygame.K_3:
                    start_time -= 10
                    upgrade_chosen = True
                    
                if upgrade_chosen:
                    wave_manager.start_next_wave()
                    if (wave_manager.current_wave_idx + 1) % 3 == 0:
                        background.next_background()
                    game_state = "PLAY"
        
        background.draw(screen)
        player_satu.draw(ctx)
        ui_manager.draw_level_up(ctx, screen_width)

    # ============================================
    # CLEANUP
    # ============================================
    surface_bridge.flush()
    del ctx
    del surface_bridge
    screen.blit(surface_cairo, (0, 0))
    pygame.display.flip()

    if game_state == "PLAY" and not paused:
        enemy_list = [e for e in enemy_list if e.is_alive]
        partikel_list = [p for p in partikel_list if p.is_alive]

    clock.tick(fps)

pygame.quit()