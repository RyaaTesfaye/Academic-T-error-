import cairo
import math
import pygame
from Settings import *

from components.hearth import create_heart
from components.scoreBoard import scoreBoard
from components.arrow import draw_arrow
from components.titleTxt import draw_title
from components.scoreBoardMenu import draw_highscore
from components.button import button
from components.gameEvent import draw_game_func

class UI:
    def __init__(self):
        self.font_family = "Arial"
    
    def draw_hud(self, ctx, player, wave_manager, screen_height, screen_width):
        ctx.set_source_rgb(*C_BLACK)
        ctx.set_font_size(20)
        wave_text = f"WAVE {wave_manager.current_wave_idx + 1}"

        ctx.move_to(screen_width / 2 - 35, 35) 
        ctx.show_text(wave_text)

        hp_padding = 10
        hp_size = 20

        for i in range(max_health_player):
            kotak_x = 20 + (i * (hp_size + hp_padding))
            kotak_y = 20
            
            if i < player.health:
                create_heart(ctx, kotak_x, kotak_y, hp_size, hp_size, C_RED_ENEMY)
                ctx.fill()
            else:
                ctx.set_source_rgb(*C_LAPTOP_GREY)
                ctx.set_line_width(2)
                create_heart(ctx, kotak_x, kotak_y, hp_size, hp_size, C_LAPTOP_GREY)
                ctx.stroke()

    def draw_scoreboard_overlay(self, ctx, live_score, is_full, arrow_x, arrow_y):
        scoreBoard(ctx, live_score, 950, 0, is_full)
        draw_arrow(ctx, arrow_x, arrow_y, direction=is_full)

    def draw_pause(self, ctx, screen_width, screen_height):
        ctx.set_source_rgba(0, 0, 0, 0.5) 
        ctx.paint()
        
        ctx.set_source_rgb(1, 1, 1) 
        ctx.select_font_face(self.font_family, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(60)
        
        text = "P A U S E D"
        (xb, yb, width, height, xa, ya) = ctx.text_extents(text)
        ctx.move_to((screen_width/2) - (width/2), screen_height/2)
        ctx.show_text(text)
        
        ctx.set_font_size(20)
        ctx.move_to((screen_width/2) - 90, (screen_height/2) + 40)
        ctx.show_text("Tekan ESC untuk Lanjut")

    def draw_menu(self, ctx, screen_width, screen_height, score_list, tombol_rect, tombol_hover, song_name):
        draw_title(ctx, screen_width / 2, 100)
        
        draw_highscore(ctx, screen_width / 3, 150, 400, 250, score_list)
        
        bg_color = C_WHITE if tombol_hover else C_LAPTOP_GREY
        text_color = (0,0,0,1) if tombol_hover else (1,1,1,1)
        
        button(ctx, tombol_rect.x + 100, tombol_rect.y - 20, tombol_rect.width, tombol_rect.height, 
               bg_color, (0.2, 0.2, 0.2, 1), "Mulai", text_color)
        
        ctx.set_source_rgb(*C_BLACK)
        ctx.set_font_size(18)
        text = f"< {song_name} >"
        (xb, yb, w, h, xa, ya) = ctx.text_extents(text)
        ctx.move_to((screen_width/2) - (w/2), tombol_rect.y + 80)
        ctx.show_text(text)

    def draw_game_over(self, ctx, screen_width, screen_height, timer_end, current_score):
        ctx.set_source_rgba(*C_RED_TRANS) 
        ctx.paint()
        
        draw_game_func(ctx, 0, 0, screen_width, screen_height, float(timer_end), current_score)


    def draw_victory(self, ctx, screen_width, screen_height, last_skor_time, current_score):
        ctx.set_source_rgba(*C_GREEN_TRANS)
        ctx.paint()

        
        draw_game_func(ctx, 0, 0, screen_width, screen_height, float(last_skor_time), current_score, True)

    def draw_level_up(self, ctx, screen_width):
        ctx.set_source_rgba(0, 0, 0, 0.8)
        ctx.paint()
        
        ctx.set_source_rgb(*C_WHITE)
        ctx.set_font_size(40)
        ctx.move_to(screen_width/2 - 150, 100)
        ctx.show_text("WAVE CLEARED!")
        
        ctx.set_source_rgb(1, 0.8, 0)
        ctx.set_font_size(25)
        ctx.move_to(screen_width/2 - 120, 150)
        ctx.show_text("PILIH UPGRADE:")
        
        card_w = 200
        card_h = 150
        gap = 20
        start_x = (screen_width - (3 * card_w + 2 * gap)) / 2
        y_pos = 200
        
        ctx.set_source_rgb(0.2, 0.8, 0.2)
        ctx.rectangle(start_x, y_pos, card_w, card_h); ctx.fill()
        ctx.set_source_rgb(*C_BLACK); ctx.set_font_size(20)
        ctx.move_to(start_x + 20, y_pos + 80); ctx.show_text("[1] HEAL +1")
        
        ctx.set_source_rgb(0.2, 0.6, 1.0)
        ctx.rectangle(start_x + card_w + gap, y_pos, card_w, card_h); ctx.fill()
        ctx.set_source_rgb(*C_BLACK)
        ctx.move_to(start_x + card_w + gap + 20, y_pos + 80); ctx.show_text("[2] RANGE +10")
        
        ctx.set_source_rgb(1.0, 0.5, 0.0)
        ctx.rectangle(start_x + (card_w + gap)*2, y_pos, card_w, card_h); ctx.fill()
        ctx.set_source_rgb(*C_BLACK)
        ctx.move_to(start_x + (card_w + gap)*2 + 20, y_pos + 80); ctx.show_text("[3] SCORE ++")