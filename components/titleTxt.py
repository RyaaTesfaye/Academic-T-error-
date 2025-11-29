import cairo
from lib.functions.hexToRGB import hex_to_rgb

def draw_title(ctx, center_x, y, text = ["AKADEMIA T(", "ERROR", ")"], color = "#ff0055"):
    ctx.select_font_face("Courier New", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(50)
    
    title_text_1 = text[0]
    title_text_2 = text[1]
    title_text_3 = text[2]
    extents1 = ctx.text_extents(title_text_1)
    extents2 = ctx.text_extents(title_text_2)
    extents3 = ctx.text_extents(title_text_3)
    
    total_width = extents1.width + extents2.width + extents3.width
    start_x = center_x - (total_width / 2)

    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(start_x, y)
    ctx.show_text(title_text_1)

    current_x = start_x + extents1.x_advance
    
    ctx.set_source_rgba(0, 1, 1, 0.5) 
    ctx.move_to(current_x - 2, y)
    ctx.show_text(title_text_2)

    ctx.set_source_rgba(1, 0, 0, 0.5)
    ctx.move_to(current_x + 2, y)
    ctx.show_text(title_text_2)

    ctx.set_source_rgba(*hex_to_rgb(color))
    ctx.move_to(current_x, y)
    ctx.show_text(title_text_2)

    current_x += extents2.x_advance
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(current_x, y)
    ctx.show_text(title_text_3)