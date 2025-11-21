import cairo

def draw_text_centered(ctx, text, x, y, font_size, font_weight=cairo.FONT_WEIGHT_NORMAL, color=(1,1,1,1), font_face="Sans"):
    ctx.select_font_face(font_face, cairo.FONT_SLANT_NORMAL, font_weight)
    ctx.set_font_size(font_size)
    
    extents = ctx.text_extents(text)
    draw_x = x - (extents.width / 2 + extents.x_bearing)
    draw_y = y 
    
    ctx.set_source_rgba(*color)
    ctx.move_to(draw_x, draw_y)
    ctx.show_text(text)