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
from components.hearth import create_heart
from components.scoreBoard import scoreBoard
from components.arrow import draw_arrow
from components.titleTxt import draw_title
from components.scoreBoardMenu import draw_highscore
from components.button import button
from components.gameEvent import draw_game_func
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
surface_bridge = cairo.ImageSurface.create_for_data(
    surface_cairo.get_buffer(),
    cairo.FORMAT_ARGB32,
    screen_width,
    screen_height
)

# ============================================
# INISIALISASI OBJEK GAME
# ============================================
player_satu = Player()
background = Background()
wave_manager = wave_managers()
enemy_list = []
partikel_list = []
current_time = 0
target_enemy = None
current_type_word = ""

# ============================================
# SETUP AUDIO - SFX
# ============================================
sfx = {}

sfx_files = {
    "laser": "lib/sfx/laser_mini.wav",
    "bomb": "lib/sfx/explosion_enem.wav",
    "glitch": "lib/sfx/glitch_char.wav"
}

# LOAD SFX FILES
for name, file_path in sfx_files.items():
    try:
        sound = pygame.mixer.Sound(file_path)
        sound.set_volume(0.7)
        sfx[name] = sound
    except Exception as e:
        sfx[name] = None

# ============================================
# SETUP AUDIO - BGM
# ============================================
try:
    pygame.mixer.music.load("lib/sfx/BGM_PERUNGGU.ogg")
    pygame.mixer.music.set_volume(0.2)
except Exception as e:
    print(f"Gagal load BGM: {e}")

# ============================================
# VARIABEL GAME STATE
# ============================================
game_state = "MENU"
last_skor_time = 0
Menu = True
Main = True
start_time = 0

# ============================================
# GAME LOOP UTAMA
# ============================================
running = True
clock = pygame.time.Clock()

while running:
    # DELTA TIME
    dt = clock.tick(fps) / 1000.0

    # CURRENT TIME
    current_time = pygame.time.get_ticks() / 1000

    # ============================================
    # EVENT HANDLING
    # ============================================
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # ============================================
    # SETUP CAIRO CONTEXT
    # ============================================
    surface_bridge = cairo.ImageSurface.create_for_data(
        surface_cairo.get_buffer(),
        cairo.FORMAT_ARGB32,
        screen_width,
        screen_height
    )
    ctx = cairo.Context(surface_bridge)
    
    # CLEAR SURFACE
    surface_cairo.fill((0, 0, 0, 0))

    # ============================================
    # STATE: PLAY
    # ============================================
    if game_state == "PLAY":

        # ============================================
        # HITUNG WAKTU GAME
        # ============================================
        game_time = (pygame.time.get_ticks() / 1000) - start_time

        # ============================================
        # INPUT KETIKAN PEMAIN
        # ============================================
        for event in events:
            if event.type == pygame.KEYDOWN:
                # DEBUG VICTORY AND LOSE
                if event.key == pygame.K_v:
                    wave_manager.is_game_cleared = True
                    enemy_list = []

                if event.key == pygame.K_l:
                    player_satu.health = 0

                # CEK TARGET ENEMY
                if target_enemy:
                    if event.unicode.isalpha():
                        pressed_letter = event.unicode.upper()
                        target_word = target_enemy.target_word.upper()
                        current_index = len(current_type_word)

                        # CEK HURUF BENAR
                        if current_index < len(target_word) and pressed_letter == target_word[current_index]:
                            current_type_word += pressed_letter

                            # PLAY SFX LASER
                            if sfx["laser"]:
                                sfx["laser"].play()

                            # SPAWN LASER PARTIKEL
                            new_laser = Laser(player_satu.x, player_satu.y, target_enemy)
                            partikel_list.append(new_laser)

                            # CEK KATA SELESAI
                            if len(current_type_word) == len(target_word):
                                target_enemy.is_alive = False

                                # PLAY SFX BOMB
                                if sfx["bomb"]:
                                    sfx["bomb"].play()

                                # SPAWN BOMB PARTIKEL
                                end_pos = (target_enemy.x, target_enemy.y)
                                new_bomb = Bomb(player_satu.x, player_satu.y, end_pos)
                                partikel_list.append(new_bomb)

                                # RESET TARGET
                                target_enemy = None
                                current_type_word = ""
                        else:
                            # SALAH KETIK - RESET
                            current_type_word = ""
                            target_enemy.speed_up()

        # ============================================
        # UPDATE PLAYER
        # ============================================
        player_satu.update(dt, sfx)
        
        # CEK PLAYER MATI
        if player_satu.health <= 0:
            game_state = "GAMEOVER"
            pygame.mixer.music.stop()

        # CEK VICTORY
        if wave_manager.is_game_cleared and len(enemy_list) == 0:
            game_state = "VICTORY"

        # UPDATE SKOR TIME
        last_skor_time = game_time

        # ============================================
        # SPAWNER ENEMY
        # ============================================
        enemy_to_spawn = wave_manager.update(dt, len(enemy_list))

        # SPAWN ENEMY JIKA ADA
        if enemy_to_spawn:
            side = random.choice(['atas', 'bawah', 'kanan', 'kiri'])
            spawn_padding = 20

            # TENTUKAN POSISI SPAWN
            if side == 'atas':
                spawn_x = random.randint(0, screen_width)
                spawn_y = -spawn_padding
            elif side == 'bawah':
                spawn_x = random.randint(0, screen_width)
                spawn_y = screen_height + spawn_padding
            elif side == 'kanan':
                spawn_x = screen_width + spawn_padding
                spawn_y = random.randint(0, screen_height)
            elif side == 'kiri':
                spawn_x = -spawn_padding
                spawn_y = random.randint(0, screen_height)

            # BUAT ENEMY BARU
            new_enemy = Enemy(spawn_x, spawn_y, enemy_to_spawn)
            enemy_list.append(new_enemy)

        # ============================================
        # UPDATE SEMUA ENEMY
        # ============================================
        for enemy in enemy_list:
            enemy.update(dt, player_satu)

        # ============================================
        # CEK TARGET ENEMY
        # ============================================
        # CEK TARGET MASIH HIDUP
        if target_enemy:
            if not target_enemy.is_alive:
                target_enemy = None
                current_type_word = ""

        # CARI TARGET TERDEKAT
        if not target_enemy:
            closest_enemy = None
            min_distance = float('inf')

            for enemy in enemy_list:
                distance = math.hypot(player_satu.x - enemy.x, player_satu.y - enemy.y)

                if distance <= player_satu.attack_range:
                    if distance < min_distance:
                        min_distance = distance
                        closest_enemy = enemy

            # SET TARGET BARU
            if closest_enemy:
                target_enemy = closest_enemy
                current_type_word = ""

        # CEK ULANG TARGET HIDUP
        if target_enemy and not target_enemy.is_alive:
            target_enemy = None

        # ============================================
        # UPDATE PARTIKEL
        # ============================================
        for partikel in partikel_list:
            partikel.update(dt)

        # ============================================
        # RENDER BACKGROUND
        # ============================================
        background.draw(ctx)

        # ============================================
        # RENDER PLAYER
        # ============================================
        player_satu.draw(ctx)

        # ============================================
        # RENDER ENEMY DAN TARGET VISUAL
        # ============================================
        for enemy in enemy_list:
            enemy.draw(ctx)

            # HIGHLIGHT TARGET ENEMY
            if enemy == target_enemy:

                # GAMBAR SOROTAN
                ctx.save()
                ctx.translate(enemy.x, enemy.y)
                ctx.set_source_rgba(*C_SOROTAN)
                ctx.set_line_width(3)
                ctx.arc(0, 0, enemy.radius + 5, 0, 2 * math.pi)
                ctx.stroke()
                ctx.restore()

                # TAMPILKAN KATA TARGET
                word_to_draw = enemy.target_word.upper()
                typed_part = ""

                if enemy == target_enemy:
                    typed_part = current_type_word

                untyped_part = word_to_draw[len(typed_part):]

                # SETUP FONT
                ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                ctx.set_font_size(16)

                # HITUNG POSISI TEKS
                (x_bearing, y_bearing, text_width, text_height, x_advance, y_advance) = ctx.text_extents(word_to_draw)
                text_x_pos = enemy.x - (text_width / 2)
                text_y_pos = enemy.y - 30

                # RENDER KATA BELUM DIKETIK
                ctx.set_source_rgb(*C_BLACK)
                ctx.move_to(text_x_pos, text_y_pos)
                ctx.show_text(" " * len(typed_part) + untyped_part)

        # ============================================
        # RENDER PARTIKEL
        # ============================================
        for partikel in partikel_list:
            partikel.draw(ctx)


        # ============================================
        # UI SCORE BOARD
        # ============================================
        if Main:
            liveScore = listScore()
            click_cooldown = 0.3
            last_click_time = 0
            Is_Full = True
            Main = False
            arrow_x, arrow_y = 1070, 60
        waktu = f"{game_time:.2f}"
        liveScore["you"] = float(waktu)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            arrow_hitbox = pygame.Rect(0, 0, 30, 30) 
            if Is_Full:
                arrow_hitbox.center = (arrow_x, arrow_y)
            else:
                arrow_hitbox.center = (arrow_x, arrow_y)

            if arrow_hitbox.collidepoint(mouse_pos):
                if current_time - last_click_time > click_cooldown:
                    Is_Full = not Is_Full
                    last_click_time = current_time
                    if Is_Full:
                        arrow_y = 60
                    else:
                        arrow_y = 217

        SxoreBoard = scoreBoard(ctx, liveScore, 950, 0, Is_Full)
        draw_arrow(ctx, arrow_x, arrow_y, direction=Is_Full)

        # ============================================
        # UI WAVE INFO
        # ============================================
        ctx.set_source_rgb(*C_BLACK)
        ctx.set_font_size(20)
        wave_text = f"WAVE {wave_manager.current_wave_idx + 1}"

        # RENDER WAVE INFO
        ctx.move_to(screen_height - 40, 40)
        ctx.show_text(wave_text)

        # ============================================
        # UI HEALTH BAR
        # ============================================
        hp_padding = 10
        hp_size = 20

        # RENDER HP BOXES
        for i in range(max_health_player):
            kotak_x = 20 + (i * (hp_size + hp_padding))
            kotak_y = 20
            
            # HP MASIH ADA
            if i < player_satu.health:
                create_heart(ctx, kotak_x, kotak_y, hp_size, hp_size, C_RED_ENEMY)
                ctx.fill()
            # HP HILANG
            else:
                ctx.set_source_rgb(*C_LAPTOP_GREY)
                ctx.set_line_width(2)
                create_heart(ctx, kotak_x, kotak_y, hp_size, hp_size, C_LAPTOP_GREY)
                ctx.stroke()

    # ============================================
    # STATE: MENU
    # ============================================
    elif game_state == "MENU":
        # ============================================
        # SETUP TOMBOL
        # ============================================
        tombol_rect = pygame.Rect((screen_width / 2), (screen_height / 2) +150, 200, 50)
        mouse_pos = pygame.mouse.get_pos()

        # CEK HOVER TOMBOL
        tombol_hover = False
        if tombol_rect.collidepoint(mouse_pos):
            tombol_hover = True

        # ============================================
        # DETEKSI KLIK TOMBOL
        # ============================================
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tombol_hover:
                    game_state = "PLAY"

                    # PLAY BGM
                    pygame.mixer.music.play(loops=-1)

                    # RESET GAME
                    player_satu = Player()
                    enemy_list = []
                    partikel_list = []
                    current_type_word = ""
                    target_enemy = None
                    last_spawn_time = current_time
                    score_calculated = False
        
        #GAMBAR BG DISINI
                    wave_manager = wave_managers()
                    start_time = pygame.time.get_ticks() / 1000

        # ============================================
        # RENDER MENU
        # ============================================
        # RENDER BACKGROUND
        background.draw(ctx)

        # RENDER JUDUL
        draw_title(ctx, screen_width / 2, 100)

        ctx.move_to(0,0)


        if Menu: 
            scoreList = listScore()
            Menu = False

        # LIST SCORE
        draw_highscore(ctx, screen_width / 3, 150, 400, 250, scoreList)
        
        # RENDER TOMBOL MULAI
        if tombol_hover:
            button(ctx, tombol_rect.x, tombol_rect.y, tombol_rect.width, tombol_rect.height, C_WHITE, (0.2, 0.2, 0.2, 1),  "Mulai", (0,0,0,1))
        else:
            button(ctx, tombol_rect.x, tombol_rect.y, tombol_rect.width, tombol_rect.height, C_LAPTOP_GREY, (0.2, 0.2, 0.2, 1),  "Mulai", (1,1,1 ,1))

        
    elif game_state == "GAMEOVER":

        global timer_end
    
        if not score_calculated:
            timer_end = highscore(last_skor_time)
            Menu = True
            Main = True
            score_calculated = True

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = "MENU"
        
        
        background.draw(ctx) 
        
        ctx.set_source_rgba(*C_RED_TRANS) 
        ctx.paint()
        draw_game_func(ctx, 0, 0, screen_width, screen_height, float(timer_end), scoreList["you"])
    

    # ============================================
    # STATE: VICTORY
    # ============================================
    elif game_state == "VICTORY":
        # ============================================
        # INPUT KEMBALI KE MENU
        # ============================================
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "MENU"

        # ============================================
        # RENDER VICTORY SCREEN
        # ============================================
        # RENDER BACKGROUND
        background.draw(ctx)

        # OVERLAY HIJAU
        ctx.set_source_rgba(*C_GREEN_TRANS)
        ctx.paint()

        draw_game_func(ctx, 0, 0, screen_width, screen_height, float(last_skor_time), scoreList["you"], True)

    # ============================================
    # CLEANUP CAIRO DAN RENDER KE SCREEN
    # ============================================
    surface_bridge.flush()
    del ctx
    del surface_bridge
    
    # BLIT KE SCREEN
    screen.blit(surface_cairo, (0, 0))
    pygame.display.flip()

    # ============================================
    # CLEANUP OBJEK MATI
    # ============================================
    if game_state == "PLAY":
        enemy_list = [e for e in enemy_list if e.is_alive]
        partikel_list = [p for p in partikel_list if p.is_alive]

    # TICK CLOCK
    clock.tick(fps)

# ============================================
# QUIT PYGAME
# ============================================
pygame.quit()