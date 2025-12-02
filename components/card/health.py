import cairo
import math
from lib.functions.rounded import rounded_rect

WIDTH, HEIGHT = 400, 600
FRAMES = 50
DURATION = 40

COLOR_BG_DARK = (0.02, 0.02, 0.02)
COLOR_CARD_BG = (0.12, 0.12, 0.16)
COLOR_ACCENT_PINK_LIGHT = (1.0, 0.42, 0.58)
COLOR_ACCENT_PINK_DARK = (0.84, 0.0, 0.3)
COLOR_ACCENT_NEON = (1.0, 0.0, 0.33)
COLOR_ACCENT_GREEN = (0.0, 1.0, 0.66)
COLOR_TEXT_SUB = (0.7, 0.7, 0.75)

def draw_grid_background(ctx, w, h):
    ctx.set_source_rgb(*COLOR_BG_DARK)
    ctx.paint()
    
    ctx.set_line_width(1)
    ctx.set_source_rgba(1, 1, 1, 0.03)
    
    grid_size = 30
    for x in range(0, w, grid_size):
        ctx.move_to(x, 0)
        ctx.line_to(x, h)
    for y in range(0, h, grid_size):
        ctx.move_to(0, y)
        ctx.line_to(w, y)
    ctx.stroke()

def draw_heart(ctx, center_x, center_y, size):
    ctx.save()
    ctx.translate(center_x, center_y)
    ctx.scale(size, size)
    
    ctx.move_to(0, -0.7)
    ctx.curve_to(0.5, -1.2, 1.3, -1.0, 1.3, -0.3)
    ctx.curve_to(1.3, 0.2, 0.6, 0.6, 0, 1.0)
    ctx.curve_to(-0.6, 0.6, -1.3, 0.2, -1.3, -0.3)
    ctx.curve_to(-1.3, -1.0, -0.5, -1.2, 0, -0.7)
    ctx.close_path()
    
    pat = cairo.LinearGradient(0, -1.5, 0, 1.0)
    pat.add_color_stop_rgb(0, *COLOR_ACCENT_PINK_LIGHT)
    pat.add_color_stop_rgb(1, *COLOR_ACCENT_PINK_DARK)
    
    ctx.set_source(pat)
    ctx.fill()
    ctx.restore()

def draw_spinning_particles(ctx, cx, cy, radius, progress):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(progress * 2 * math.pi)
    
    ctx.set_line_width(1)
    ctx.set_source_rgba(1, 1, 1, 0.1)
    ctx.set_dash([5, 5])
    ctx.arc(0, 0, radius, 0, 2 * math.pi)
    ctx.stroke()
    
    ctx.set_dash([])
    ctx.set_source_rgb(*COLOR_ACCENT_NEON)
    ctx.arc(radius, 0, 2, 0, 2 * math.pi)
    ctx.fill()
    
    ctx.restore()

def drawHealthCard(ctx, x, y, w, h, progress):
    s = w / 300.0  
    
    center_x = x + (w / 2)
    
    pulse = (math.sin(progress * 2 * math.pi * 2) + 1) / 2 
    heart_scale = 1.0 + (pulse * 0.15)
    
    ctx.save()
    rounded_rect(ctx, x, y + (10 * s), w, h, 20 * s)
    ctx.set_source_rgba(*COLOR_ACCENT_NEON, 0.1 + (pulse * 0.1))
    ctx.fill()
    ctx.restore()

    rounded_rect(ctx, x, y, w, h, 20 * s)
    ctx.set_source_rgba(30/255, 30/255, 40/255, 0.95)
    ctx.fill()

    ctx.save()
    rounded_rect(ctx, x, y, w, h, 20 * s)
    grad_border = cairo.LinearGradient(x, y, x + w, y)
    grad_border.add_color_stop_rgba(0, 1, 1, 1, 0.1)
    grad_border.add_color_stop_rgba(0.5, *COLOR_ACCENT_NEON, 0.5)
    grad_border.add_color_stop_rgba(1, 1, 1, 1, 0.1)
    ctx.set_source(grad_border)
    ctx.set_line_width(2 * s)
    ctx.stroke()
    ctx.restore()

    ctx.move_to(x + (20 * s), y)
    ctx.line_to(x + w - (20 * s), y)
    ctx.set_source_rgba(*COLOR_ACCENT_NEON, 0.5)
    ctx.set_line_width(4 * s)
    ctx.stroke()

    text_y_base = y + (h * 0.15)
    
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(32 * s) 
    txt_title = "HATI"
    ext_t = ctx.text_extents(txt_title)
    
    grad_text = cairo.LinearGradient(0, text_y_base - (30*s), 0, text_y_base)
    grad_text.add_color_stop_rgb(0, *COLOR_ACCENT_PINK_LIGHT)
    grad_text.add_color_stop_rgb(1, *COLOR_ACCENT_NEON)
    
    ctx.move_to(center_x - (ext_t.width / 2), text_y_base)
    ctx.set_source(grad_text)
    ctx.show_text(txt_title)

    ctx.set_font_size(14 * s)
    txt_sub = "HATI YANG BENAR BENAR SUCI"
    ext_s = ctx.text_extents(txt_sub)
    ctx.move_to(center_x - (ext_s.width / 2), text_y_base + (25 * s))
    ctx.set_source_rgba(*COLOR_TEXT_SUB, 0.8)
    ctx.show_text(txt_sub)

    heart_cy = y + (h * 0.42) 
    heart_base_radius = 35 * s
    
    bg_heart_radius = (60 * s) + (pulse * 5 * s)
    ctx.arc(center_x, heart_cy, bg_heart_radius, 0, 2*math.pi)
    ctx.set_source_rgba(*COLOR_ACCENT_NEON, 0.15)
    ctx.fill()
    
    draw_spinning_particles(ctx, center_x, heart_cy, 70 * s, progress)

    draw_heart(ctx, center_x, heart_cy, heart_base_radius * heart_scale)

    box_w_real = w - (60 * s)
    box_h_real = h * 0.17    
    box_x = x + (w - box_w_real) / 2
    box_y = y + (h * 0.63)
    
    rounded_rect(ctx, box_x, box_y, box_w_real, box_h_real, 12 * s)
    ctx.set_source_rgba(0, 0, 0, 0.4)
    ctx.fill()
    
    ctx.move_to(box_x + (20 * s), box_y + box_h_real)
    ctx.line_to(box_x + box_w_real - (20 * s), box_y + box_h_real)
    ctx.set_source_rgba(*COLOR_ACCENT_GREEN, 0.6)
    ctx.set_line_width(2 * s)
    ctx.stroke()

    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(32 * s)
    txt_hp = "+1 HP"
    ext_hp = ctx.text_extents(txt_hp)
    
    text_hp_y = box_y + (box_h_real * 0.5)
    ctx.move_to(center_x - (ext_hp.width / 2), text_hp_y)
    ctx.set_source_rgb(*COLOR_ACCENT_GREEN)
    ctx.show_text(txt_hp)
    
    ctx.set_font_size(11 * s)
    txt_desc = "MENAMBAH DARAH"
    ext_desc = ctx.text_extents(txt_desc)
    
    text_desc_y = box_y + (box_h_real * 0.8)
    ctx.move_to(center_x - (ext_desc.width / 2), text_desc_y)
    ctx.set_source_rgba(1, 1, 1, 0.7)
    ctx.show_text(txt_desc)

    footer_y = y + h - (40 * s)
    
    footer_font_size = 12 * s
    ctx.set_font_size(footer_font_size)
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    
    txt_1 = "KETIK"
    txt_2 = "UNTUK MEMILIH"
    txt_btn = "1"
    
    w_text1 = ctx.text_extents(txt_1).width
    w_text2 = ctx.text_extents(txt_2).width
    w_btn_bg = 24 * s
    padding = 8 * s
    
    total_footer_width = w_text1 + padding + w_btn_bg + padding + w_text2
    cursor_x = center_x - (total_footer_width / 2)
    
    ctx.set_source_rgba(*COLOR_TEXT_SUB, 0.9)
    ctx.move_to(cursor_x, footer_y)
    ctx.show_text(txt_1)
    
    cursor_x += w_text1 + padding
    
    btn_h = 20 * s
    btn_y = footer_y - (btn_h * 0.75)
    rounded_rect(ctx, cursor_x, btn_y, w_btn_bg, btn_h, 5 * s)
    ctx.set_source_rgba(1, 1, 1, 0.1)
    ctx.fill_preserve()
    ctx.set_source_rgba(1, 1, 1, 0.3)
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