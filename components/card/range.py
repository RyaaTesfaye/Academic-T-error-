import cairo
import math
from lib.functions.rounded import rounded_rect

WIDTH, HEIGHT = 400, 600
FRAMES = 50          
DURATION = 40        

COLOR_BG_DARK = (0.02, 0.02, 0.05)
COLOR_CARD_BG = (0.12, 0.14, 0.18)
COLOR_ACCENT_LIGHT = (0.42, 0.85, 1.0)
COLOR_ACCENT_DARK = (0.0, 0.3, 0.8)
COLOR_ACCENT_NEON = (0.0, 0.9, 1.0)
COLOR_ACCENT_STATS = (1.0, 0.8, 0.0)
COLOR_TEXT_SUB = (0.6, 0.7, 0.8)

def draw_grid_background(ctx, w, h):
    ctx.set_source_rgb(*COLOR_BG_DARK)
    ctx.paint()
    
    ctx.set_line_width(1)
    ctx.set_source_rgba(0, 1, 1, 0.03)
    
    grid_size = 30
    for x in range(0, w, grid_size):
        ctx.move_to(x, 0)
        ctx.line_to(x, h)
    for y in range(0, h, grid_size):
        ctx.move_to(0, y)
        ctx.line_to(w, y)
    ctx.stroke()

def draw_scope_icon(ctx, center_x, center_y, size, rotation):
    ctx.save()
    ctx.translate(center_x, center_y)
    ctx.scale(size, size)
    
    ctx.rotate(rotation)

    ctx.new_sub_path()
    ctx.arc(0, 0, 1.0, 0, 2 * math.pi)
    ctx.set_source_rgba(*COLOR_ACCENT_NEON, 0.8)
    ctx.set_line_width(0.05)
    ctx.set_dash([0.2, 0.1])
    ctx.stroke()
    ctx.set_dash([])

    ctx.new_sub_path()
    ctx.arc(0, 0, 0.6, 0, 2 * math.pi)
    ctx.set_line_width(0.08)
    ctx.stroke()

    ctx.set_line_width(0.15)
    ctx.move_to(-1.4, 0)
    ctx.line_to(-0.3, 0)
    ctx.move_to(0.3, 0)
    ctx.line_to(1.4, 0)
    ctx.move_to(0, -1.4)
    ctx.line_to(0, -0.3)
    ctx.move_to(0, 0.3)
    ctx.line_to(0, 1.4)
    ctx.stroke()

    ctx.new_sub_path()
    ctx.arc(0, 0, 0.15, 0, 2*math.pi)
    ctx.set_source_rgb(*COLOR_ACCENT_LIGHT)
    ctx.fill()
    
    ctx.set_source_rgba(*COLOR_ACCENT_NEON, 0.5)
    for angle in [45, 135, 225, 315]:
        rad = math.radians(angle)
        dist = 0.8
        ctx.save()
        ctx.rotate(rad)
        ctx.translate(dist, 0)
        ctx.move_to(0, 0)
        ctx.line_to(-0.1, 0.05)
        ctx.line_to(-0.1, -0.05)
        ctx.fill()
        ctx.restore()

    ctx.restore()

def draw_radar_scan(ctx, cx, cy, radius, angle):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(angle)
    
    pat = cairo.RadialGradient(0, 0, 0, 0, 0, radius)
    pat.add_color_stop_rgba(0, *COLOR_ACCENT_NEON, 0)
    pat.add_color_stop_rgba(1, *COLOR_ACCENT_NEON, 0.1)
    
    ctx.move_to(0, 0)
    ctx.arc(0, 0, radius, 0, math.pi/4)
    ctx.close_path()
    
    ctx.set_source_rgba(*COLOR_ACCENT_NEON, 0.2)
    ctx.fill()
    ctx.restore()

def drawCardRange(ctx, x, y, w, h, progress):
    s = w / 300.0  
    center_x = x + (w / 2)
    
    rot_scope = progress * math.pi
    pulse = (math.sin(progress * 2 * math.pi) + 1) / 2
    glow_opacity = 0.1 + (pulse * 0.15)

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
    txt_title = "RADAR"
    ext_t = ctx.text_extents(txt_title)
    
    grad_text = cairo.LinearGradient(0, text_y_base - (30*s), 0, text_y_base)
    grad_text.add_color_stop_rgb(0, *COLOR_ACCENT_LIGHT)
    grad_text.add_color_stop_rgb(1, *COLOR_ACCENT_NEON)
    
    ctx.move_to(center_x - (ext_t.width / 2), text_y_base)
    ctx.set_source(grad_text)
    ctx.show_text(txt_title)

    ctx.set_font_size(14 * s)
    txt_sub = "MENDETEKSI MUSUH LEBIH CEPAT"
    ext_s = ctx.text_extents(txt_sub)
    ctx.move_to(center_x - (ext_s.width / 2), text_y_base + (25 * s))
    ctx.set_source_rgba(*COLOR_TEXT_SUB, 0.9)
    ctx.show_text(txt_sub)

    icon_cy = y + (h * 0.42)
    icon_bg_radius = 65 * s
    
    ctx.arc(center_x, icon_cy, icon_bg_radius, 0, 2*math.pi)
    ctx.set_source_rgba(*COLOR_ACCENT_DARK, 0.3)
    ctx.fill()
    
    draw_radar_scan(ctx, center_x, icon_cy, 60 * s, progress * -4 * math.pi)

    draw_scope_icon(ctx, center_x, icon_cy, 40 * s, rot_scope)

    box_w_real = w - (60 * s)
    box_h_real = h * 0.17
    box_x = x + (w - box_w_real) / 2
    box_y = y + (h * 0.63)
    
    rounded_rect(ctx, box_x, box_y, box_w_real, box_h_real, 12 * s)
    ctx.set_source_rgba(0, 0, 0, 0.4)
    ctx.fill()
    
    ctx.move_to(box_x + (20 * s), box_y + box_h_real)
    ctx.line_to(box_x + box_w_real - (20 * s), box_y + box_h_real)
    ctx.set_source_rgba(*COLOR_ACCENT_STATS, 0.7)
    ctx.set_line_width(2 * s)
    ctx.stroke()

    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(32 * s)
    txt_hp = "+10 RANGE"
    ext_hp = ctx.text_extents(txt_hp)
    
    text_hp_y = box_y + (box_h_real * 0.5)
    ctx.move_to(center_x - (ext_hp.width / 2), text_hp_y)
    ctx.set_source_rgb(*COLOR_ACCENT_STATS) 
    ctx.show_text(txt_hp)
    
    ctx.set_font_size(11 * s)
    txt_desc = "MENAMBAH JARAK TEMBAK"
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
    txt_btn = "2"
    
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