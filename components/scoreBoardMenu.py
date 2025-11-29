from lib.functions.rounded import rounded_rect
from lib.functions.hexToRGB import hex_to_rgb
import cairo

def draw_highscore(ctx, x, y, w, h, scores):
    ctx.set_source_rgba(1, 1, 1, 0.5)
    rounded_rect(ctx, x, y, w, h, 10)
    ctx.fill_preserve()
    
    ctx.set_source_rgba(*hex_to_rgb("#7a9c68"))
    ctx.set_line_width(3)
    ctx.stroke()

    ctx.set_source_rgba(*hex_to_rgb("#333333"))
    ctx.select_font_face("Courier New", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(24)
    
    ctx.move_to(x + 20, y + 40)
    ctx.show_text("High Score:")
    
    ctx.set_dash([5.0])
    ctx.move_to(x + 20, y + 50)
    ctx.line_to(x + w - 20, y + 50)
    ctx.stroke()
    ctx.set_dash([])

    list_start_y = y + 90
    line_height = 30

    for i, data in enumerate(scores):
        y_pos = list_start_y + (i * line_height)

        if data.startswith("you"):
            ctx.set_source_rgba(0, 0, 0, 0.1)
            ctx.rectangle(x + 10, y_pos - 20, w - 20, 25)
            ctx.fill()
            ctx.select_font_face("Courier New", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            ctx.set_source_rgb(0, 0, 0)
        else:
            ctx.select_font_face("Courier New", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            ctx.set_source_rgba(*hex_to_rgb("#333333"))

        ctx.move_to(x + 20, y_pos)
        ctx.show_text(str(i+1) + ". " +data)

        score_extents = ctx.text_extents(str(scores[data]))
        ctx.move_to(x + w - 20 - score_extents.width, y_pos)
        ctx.show_text(str(scores[data]))
