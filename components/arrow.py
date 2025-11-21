from lib.functions.hexToRGB import hex_to_rgb

def draw_arrow(ctx, x, y, size=10, direction=True, color="#3E2723"):
    ctx.save()
    ctx.translate(x, y)
    
    if direction == False:
        ctx.rotate(3.14159)
    
    ctx.set_source_rgba(*hex_to_rgb(color))
    ctx.move_to(0, size/2)
    ctx.line_to(-size, -size/2)
    ctx.line_to(size, -size/2)
    ctx.close_path()
    ctx.fill()
    ctx.restore()