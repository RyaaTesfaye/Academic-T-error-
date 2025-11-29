from lib.functions.rounded import rounded_rect
import cairo


def button(ctx, center_x, y, w, h, color_btn, color_bayangan_btn, text, color_text):
    btn_x = center_x - (w / 2)
    
    ctx.set_source_rgba(*color_bayangan_btn)
    rounded_rect(ctx, btn_x, y + 4, w, h, 5)
    ctx.fill()

    ctx.set_source_rgba(*color_btn)
    rounded_rect(ctx, btn_x, y, w, h, 5)
    ctx.fill()

    ctx.set_source_rgba(*color_text)
    ctx.select_font_face("Courier New", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(28)
    
    btn_text = text
    text_ext = ctx.text_extents(btn_text)
    
    text_x = btn_x + (w - text_ext.width) / 2
    text_y = y + (h + text_ext.height) / 2 - 5
    
    ctx.move_to(text_x, text_y)
    ctx.show_text(btn_text)
