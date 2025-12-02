import cairo
import math
import random
from lib.functions.rounded import rounded_rect
WIDTH, HEIGHT = 400, 600
FRAMES = 50          
DURATION = 40        

COLOR_BG_DARK = (0.05, 0.02, 0.0)
COLOR_CARD_BG = (0.18, 0.10, 0.05)
COLOR_ACCENT_LIGHT = (1.0, 0.9, 0.6)
COLOR_ACCENT_DARK = (0.6, 0.3, 0.0)
COLOR_ACCENT_NEON = (1.0, 0.6, 0.0)
COLOR_ACCENT_STATS = (1.0, 1.0, 0.8)
COLOR_TEXT_SUB = (0.8, 0.7, 0.6)

SPARKLES = [(random.random() * 100 - 50, random.random() * 100 - 50, random.random()) for _ in range(10)]

def draw_star_icon(ctx, center_x, center_y, size, rotation):
    ctx.save()
    ctx.translate(center_x, center_y)
    ctx.rotate(rotation)
    ctx.scale(size, size)

    ctx.new_sub_path()
    points = 5
    outer_rad = 1.0
    inner_rad = 0.45
    for i in range(points * 2):
        angle = (i * math.pi) / points
        r = outer_rad if i % 2 == 0 else inner_rad
        x = r * math.sin(angle)
        y = -r * math.cos(angle)
        if i == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)
    ctx.close_path()
    
    pat = cairo.RadialGradient(0, 0, 0, 0, 0, 1.0)
    pat.add_color_stop_rgb(0, *COLOR_ACCENT_LIGHT)
    pat.add_color_stop_rgb(1, *COLOR_ACCENT_NEON)
    ctx.set_source(pat)
    ctx.fill_preserve()
    
    ctx.set_source_rgba(1, 1, 1, 0.8)
    ctx.set_line_width(0.05)
    ctx.stroke()

    ctx.restore()

def draw_coin_ring(ctx, cx, cy, radius, rotation, scale_factor):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(rotation)
    
    ctx.new_sub_path()
    ctx.arc(0, 0, radius, 0, 2*math.pi)
    ctx.set_source_rgba(*COLOR_ACCENT_NEON, 0.3)
    ctx.set_line_width(2 * scale_factor) 
    ctx.stroke()
    
    count = 8
    dot_radius = 4 * scale_factor
    for i in range(count):
        angle = (i / count) * 2 * math.pi
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        
        ctx.new_sub_path()
        ctx.arc(x, y, dot_radius, 0, 2*math.pi)
        ctx.set_source_rgb(*COLOR_ACCENT_LIGHT)
        ctx.fill()
        
    ctx.restore()

def drawCardScore(ctx, x, y, w, h, progress):
    s = w / 300.0
    center_x = x + (w / 2)
    
    rot_star = progress * 2 * math.pi 
    rot_ring = -progress * math.pi    
    pulse = (math.sin(progress * 2 * math.pi) + 1) / 2
    glow_opacity = 0.1 + (pulse * 0.2)

    ctx.save()
    rounded_rect(ctx, x, y + (10 * s), w, h, 20 * s)
    ctx.set_source_rgba(*COLOR_ACCENT_NEON, glow_opacity)
    ctx.fill()
    ctx.restore()

    rounded_rect(ctx, x, y, w, h, 20 * s)
    ctx.set_source_rgba(*COLOR_CARD_BG, 0.95)
    ctx.fill()

    ctx.save()
    rounded_rect(ctx, x, y, w, h, 20 * s)
    grad_border = cairo.LinearGradient(x, y, x + w, y)
    grad_border.add_color_stop_rgba(0, *COLOR_ACCENT_DARK, 0.3)
    grad_border.add_color_stop_rgba(0.5, *COLOR_ACCENT_NEON, 0.8)
    grad_border.add_color_stop_rgba(1, *COLOR_ACCENT_DARK, 0.3)
    ctx.set_source(grad_border)
    ctx.set_line_width(2 * s)
    ctx.stroke()
    ctx.restore()

    ctx.move_to(x + (20 * s), y)
    ctx.line_to(x + w - (20 * s), y)
    ctx.set_source_rgba(*COLOR_ACCENT_NEON, 0.6)
    ctx.set_line_width(4 * s)
    ctx.stroke()

    text_y_base = y + (h * 0.15)
    
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(32 * s)
    txt_title = "SKOR"
    ext_t = ctx.text_extents(txt_title)
    
    grad_text = cairo.LinearGradient(0, text_y_base - (30*s), 0, text_y_base)
    grad_text.add_color_stop_rgb(0, *COLOR_ACCENT_LIGHT)
    grad_text.add_color_stop_rgb(1, *COLOR_ACCENT_NEON)
    
    ctx.move_to(center_x - (ext_t.width / 2), text_y_base)
    ctx.set_source(grad_text)
    ctx.show_text(txt_title)

    ctx.set_font_size(14 * s)
    txt_sub = "SKOR YANG DIAMBIL DARI BINTANG"
    ext_s = ctx.text_extents(txt_sub)
    ctx.move_to(center_x - (ext_s.width / 2), text_y_base + (25 * s))
    ctx.set_source_rgba(*COLOR_TEXT_SUB, 0.9)
    ctx.show_text(txt_sub)

    icon_cy = y + (h * 0.42)
    icon_bg_radius = 65 * s
    
    ctx.arc(center_x, icon_cy, icon_bg_radius, 0, 2*math.pi)
    ctx.set_source_rgba(*COLOR_ACCENT_DARK, 0.4)
    ctx.fill()
    
    draw_coin_ring(ctx, center_x, icon_cy, 55 * s, rot_ring, s)

    draw_star_icon(ctx, center_x, icon_cy, 35 * s, rot_star)
    
    for i, (sx, sy, offset) in enumerate(SPARKLES):
        alpha = (math.sin((progress + offset) * 4 * math.pi) + 1) / 2
        
        sp_x = center_x + (sx * s)
        sp_y = icon_cy + (sy * s)
        sp_rad = 2 * s

        ctx.new_sub_path()
        ctx.arc(sp_x, sp_y, sp_rad, 0, 2*math.pi)
        ctx.set_source_rgba(1, 1, 0.8, alpha * 0.8)
        ctx.fill()

    box_w_real = w - (60 * s)
    box_h_real = h * 0.17
    box_x = x + (w - box_w_real) / 2
    box_y = y + (h * 0.63)
    
    rounded_rect(ctx, box_x, box_y, box_w_real, box_h_real, 12 * s)
    ctx.set_source_rgba(0, 0, 0, 0.4)
    ctx.fill()
    
    ctx.move_to(box_x + (20 * s), box_y + box_h_real)
    ctx.line_to(box_x + box_w_real - (20 * s), box_y + box_h_real)
    ctx.set_source_rgba(*COLOR_ACCENT_NEON, 0.7)
    ctx.set_line_width(2 * s)
    ctx.stroke()

    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(32 * s)
    txt_hp = "SCORE ++"
    ext_hp = ctx.text_extents(txt_hp)
    
    text_hp_y = box_y + (box_h_real * 0.5)
    ctx.move_to(center_x - (ext_hp.width / 2), text_hp_y)
    ctx.set_source_rgb(*COLOR_ACCENT_STATS) 
    ctx.show_text(txt_hp)
    
    ctx.set_font_size(11 * s)
    txt_desc = "MENAMBAH SKOR"
    ext_desc = ctx.text_extents(txt_desc)
    
    text_desc_y = box_y + (box_h_real * 0.8)
    ctx.move_to(center_x - (ext_desc.width / 2), text_desc_y)
    ctx.set_source_rgba(1, 1, 1, 0.7)
    ctx.show_text(txt_desc)

    footer_y = y + h - (40 * s)
    
    ctx.set_font_size(12 * s)
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    
    txt_1 = "KETIK"
    txt_2 = "UNTUK MEMILIH"
    txt_btn = "3"
    
    w_text1 = ctx.text_extents(txt_1).width
    w_text2 = ctx.text_extents(txt_2).width
    w_btn_bg = 24 * s
    padding = 8 * s
    
    total_footer_w = w_text1 + padding + w_btn_bg + padding + w_text2
    cursor_x = center_x - (total_footer_w / 2)
    
    ctx.set_source_rgba(*COLOR_TEXT_SUB, 0.9)
    ctx.move_to(cursor_x, footer_y)
    ctx.show_text(txt_1)
    
    cursor_x += w_text1 + padding
    
    btn_h = 20 * s
    btn_y = footer_y - (btn_h * 0.75)
    
    rounded_rect(ctx, cursor_x, btn_y, w_btn_bg, btn_h, 5 * s)
    ctx.set_source_rgba(*COLOR_ACCENT_NEON, 0.1) 
    ctx.fill_preserve()
    ctx.set_source_rgba(*COLOR_ACCENT_NEON, 0.4) 
    ctx.set_line_width(1 * s)
    ctx.stroke()
    
    w_num = ctx.text_extents(txt_btn).width
    num_x = cursor_x + (w_btn_bg / 2) - (w_num / 2)
    
    ctx.set_source_rgb(*COLOR_ACCENT_NEON)
    ctx.move_to(num_x, footer_y)
    ctx.show_text(txt_btn)
    
    cursor_x += w_btn_bg + padding
    
    ctx.set_source_rgba(*COLOR_TEXT_SUB, 0.9)
    ctx.move_to(cursor_x, footer_y)
    ctx.show_text(txt_2)