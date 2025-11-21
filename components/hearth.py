def create_heart(ctx, x, y, width, height, warna):
    ctx.save()
    ctx.translate(x, y)
    scale_x = width / 64.0
    scale_y = height / 64.0
    ctx.scale(scale_x, scale_y)
    ctx.set_source_rgb(*warna)
    ctx.move_to(32, 15)
    ctx.curve_to(32, 0,   0, 0,   0, 24)
    ctx.curve_to(0, 42,  16, 54,  32, 62)
    ctx.curve_to(48, 54, 64, 42,  64, 24)
    ctx.curve_to(64, 0,  32, 0,   32, 15)
    ctx.close_path()
    ctx.fill()

    ctx.restore()