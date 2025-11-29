import cairo
from lib.functions.hexToRGB import hex_to_rgb
from lib.functions.rounded import rounded_rect
from lib.functions.drawTextCenter import draw_text_centered
from components.titleTxt import draw_title

def draw_game_func(ctx, x, y, width, height, score, high_score, victory = False):

    if victory:
        text = ["", "VICTORY", ""]
        color = "#006f41"
    else:
        text =  ["Game ", "Over", ""]
        color = "#ff0055"
    center_x = width / 2
    
    if score > high_score:
        label_top = "REKOR BARU!"
        label_color = hex_to_rgb("#d4af37")
        display_hs_val = f"{score:.2f}"
    else:
        label_top = "SKOR KAMU:"
        label_color = (0.33, 0.33, 0.33)
        display_hs_val = f"{high_score:.2f}"

    score_text = f"{score:.2f}"

    card_w, card_h = 480, 320
    card_x, card_y = center_x - card_w / 2, 140
    radius = 8

    draw_title(ctx, center_x, 100,text, color)

    for off, col in [(12, (0, 0, 0, 0.15)), (0, (240/255, 240/255, 240/255, 0.95))]:
        ctx.set_source_rgba(*col)
        rounded_rect(ctx, card_x + off, card_y + off, card_w, card_h, radius)
        ctx.fill()

    ctx.set_source_rgba(*hex_to_rgb(color))
    ctx.set_line_width(4)
    rounded_rect(ctx, card_x, card_y, card_w, card_h, radius)
    ctx.stroke()

    draw_text_centered(ctx, label_top, center_x, card_y + 60, 16, cairo.FONT_WEIGHT_BOLD, label_color)

    ctx.set_font_size(48)
    ctx.select_font_face("Courier New", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ext = ctx.text_extents(score_text)

    hl_y = card_y + 80
    ctx.rectangle(center_x - ext.width/2 - 20, hl_y, ext.width + 40, ext.height + 20)
    ctx.set_source_rgba(*hex_to_rgb("#d4d4d4"))
    ctx.fill()

    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(center_x - ext.width/2, hl_y + ext.height + 5)
    ctx.show_text(score_text)

    line_y = hl_y + ext.height + 50
    ctx.set_source_rgb(0.6, 0.6, 0.6)
    ctx.set_line_width(2)
    ctx.set_dash([10.0])
    ctx.move_to(card_x + 40, line_y)
    ctx.line_to(card_x + card_w - 40, line_y)
    ctx.stroke()
    ctx.set_dash([])

    hs_label = "HIGH SCORE: "
    hs_y = line_y + 40
    
    ctx.set_font_size(20)
    ctx.select_font_face("Courier New", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    w_label = ctx.text_extents(hs_label).width
    
    ctx.select_font_face("Courier New", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    w_val = ctx.text_extents(display_hs_val).width
    
    start_x = center_x - (w_label + w_val) / 2

    ctx.select_font_face("Courier New", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_source_rgb(0.2, 0.2, 0.2)
    ctx.move_to(start_x, hs_y)
    ctx.show_text(hs_label)
    
    ctx.select_font_face("Courier New", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_source_rgba(*hex_to_rgb("#6b8e4e"))
    ctx.move_to(start_x + w_label, hs_y)
    ctx.show_text(display_hs_val)

    draw_text_centered(ctx, "[ Tekan ENTER untuk Menu ]", center_x, hs_y + 80, 14, cairo.FONT_WEIGHT_NORMAL, (0.4, 0.4, 0.4))