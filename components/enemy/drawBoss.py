import random
import math
import cairo

# --- KONFIGURASI WARNA & KONSTANTA ---
BG_BASE = (0.02, 0.02, 0.02)
FOG_COLOR = (0.08, 0.08, 0.1)
ENTITY_COLOR = (0.1, 0.1, 0.1)
ERROR_RED = (1.0, 0.2, 0.2)
GLITCH_CYAN = (0.0, 1.0, 1.0)

def draw_rounded_rect(ctx, x, y, w, h, r):
    ctx.new_path()
    ctx.arc(x + w - r, y + r, r, -math.pi/2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi/2)
    ctx.arc(x + r, y + h - r, r, math.pi/2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3*math.pi/2)
    ctx.close_path()

def kabut(ctx):
    for _ in range(15):
        radius = random.randint(20, 80) 
        fx = random.randint(-150, 150)
        fy = random.randint(-150, 150)
        
        ctx.set_source_rgba(*FOG_COLOR, 0.05) 
        ctx.arc(fx, fy, radius, 0, 2 * math.pi)
        ctx.fill()

def body(ctx, points):
    ctx.move_to(*points[0])
    for point in points[1:]:
        ctx.line_to(*point)
    ctx.close_path()
    
    ctx.set_source_rgb(*ENTITY_COLOR)
    ctx.fill_preserve()
    ctx.set_source_rgba(*GLITCH_CYAN, 0.5)
    ctx.stroke()

def bodyFull(ctx):
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_width(2)
    upper_body = [(-80, -60), (80, -60), (60, 40), (-60, 40)]
    body(ctx, upper_body)
    lower_body = [(-55, 40), (55, 40), (45, 150), (-45, 150)]
    body(ctx, lower_body)

def kepalaMata(ctx, frame_index):
    head_y = -135
    head_w = 110
    head_h = 100
    r = 15
    
    ctx.save()
    ctx.translate(0, head_y)
    
    hx, hy = -head_w/2, 0
    draw_rounded_rect(ctx, hx, hy, head_w, head_h, r)
    ctx.set_source_rgb(0, 0, 0)
    ctx.fill_preserve()
    ctx.set_source_rgb(*ENTITY_COLOR)
    ctx.set_line_width(4)
    ctx.stroke()

    draw_rounded_rect(ctx, hx, hy, head_w, head_h, r)
    ctx.clip()

    scan_range = 60
    eye_y_pos = 20 + (scan_range/2) + math.sin(frame_index * 0.3) * (scan_range/2)

    ctx.rectangle(-50, eye_y_pos, 100, 10)
    ctx.set_source_rgb(*ERROR_RED)
    ctx.fill()

    ctx.rectangle(-55, eye_y_pos - 5, 110, 20)
    ctx.set_source_rgba(*ERROR_RED, 0.4)
    ctx.fill()

    ctx.restore()

def glitchEffect(ctx):
    def glitch(bounds_x, bounds_y, color):
        for _ in range(random.randint(5, 12)):
            w = random.randint(10, 40)
            h = random.randint(2, 6)
            gx = random.randint(bounds_x[0], bounds_x[1])
            gy = random.randint(bounds_y[0], bounds_y[1])
            
            ctx.set_source_rgba(*color, random.uniform(0.6, 0.9))
            ctx.rectangle(gx, gy, w, h)
            ctx.fill()

    bounds_x = (-90, 90)
    bounds_y = (-180, 160)
    glitch(bounds_x, bounds_y, GLITCH_CYAN)
    glitch(bounds_x, bounds_y, ERROR_RED)

def drawBoss(ctx, frame_index, x, y, scale=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(scale, scale)
    kabut(ctx)
    bodyFull(ctx)
    kepalaMata(ctx, frame_index)
    glitchEffect(ctx)

    ctx.restore()