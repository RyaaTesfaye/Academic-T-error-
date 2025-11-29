import cairo
import math
from Settings import *


class Background:
    def __init__(self):
        pass

    def draw(self, ctx):

        ctx.set_source_rgb(*C_BG_SKY)
        ctx.rectangle(0, 0, screen_width, screen_height)
        ctx.fill()

        ctx.set_source_rgb(*C_BG_GRASS)
        ctx.rectangle(0, 200, screen_width, 400) 
        ctx.fill()
        
        ctx.set_source_rgb(*C_BG_PAVING)
        ctx.rectangle(0, 350, screen_width, 80)
        ctx.fill()

        block_w = 40
        y = 430 
        toggle = True
        for x in range(0, screen_width, block_w):
            if toggle:
                ctx.set_source_rgb(*C_BG_BORDER_BLUE)
            else:
                ctx.set_source_rgb(*C_WHITE)

            ctx.rectangle(x, y, block_w, 25)
            ctx.fill()
            toggle = not toggle
            
    def draw_sts(self, ctx):
        #layer dasar
        ctx.set_source_rgb(0.78, 0.78, 0.78) 
        ctx.rectangle(0, 0, screen_width, screen_height)
        ctx.fill()
        
        #paving
        PAVING_W = 5   
        PAVING_H = 3  
        GAP = 0.5        
        
        #Warna balok 
        ctx.set_source_rgb(0.65, 0.65, 0.65) 

        step_x = PAVING_W + GAP
        step_y = PAVING_H + GAP
        
        #jumlah baris dan kolom
        num_rows = int(screen_height / step_y) + 2
        num_cols = int(screen_width / step_x) + 2

        #Grid Paving
        for r in range(num_rows):
            y_pos = (r * step_y)

            offset_x = 0
            if r % 2 == 1:
                offset_x = -(step_x / 2)
            
            for c in range(num_cols):
                x_pos = (c * step_x) + offset_x
                ctx.rectangle(x_pos, y_pos, PAVING_W, PAVING_H)
        ctx.fill()

        #lapangan hijau
        w, h = 1100, 500
        x_field = (screen_width - w) / 2
        y_field = (screen_height - h) / 2

        ctx.set_source_rgb(0, 0.5, 0)
        ctx.rectangle(x_field, y_field, w, h)
        ctx.fill()
        
        KERB_THICKNESS = 8 
        SEGMENT_LEN = 40   

        ctx.set_line_width(KERB_THICKNESS)
        ctx.set_source_rgb(0.9, 0.9, 0.9)
        ctx.rectangle(x_field, y_field, w, h)
        ctx.stroke()

        ctx.set_source_rgb(0.0, 0.2, 0.8) 
        ctx.set_dash([SEGMENT_LEN, SEGMENT_LEN], 0) 
        ctx.rectangle(x_field, y_field, w, h)
        ctx.stroke()

        ctx.set_dash([], 0)

        #hiasan lapangan
        ctx.set_source_rgb(0.8, 0.8, 0.2)
        pixels = [
            (300, 250), (500, 270), (700, 260),
            (400, 400), (600, 420), (800, 390),
            (450, 320), (550, 350), (650, 330),
            (950, 370), (250, 340), (1050, 280),
        ]

        for (px, py) in pixels:
            ctx.rectangle(px, py, 3, 3)
            ctx.fill()

        #wit witan
        tree_positions = [
            (100, 100),  
            (100, 300), 
            (100, 500),
            (1000, 100),
            (1000, 300),
            (1000, 500),    
        ]

        for (x, y) in tree_positions:
            #shadow
            ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
            ctx.arc(x + 10, y + 10, 30, 0, 2 * math.pi)
            ctx.fill()

            #batang
            ctx.set_source_rgb(0.4, 0.2, 0.1) 
            ctx.arc(x, y, 6, 0, 2 * math.pi)
            ctx.fill()

            #kanopi
            ctx.set_source_rgb(0.1, 0.4, 0.1) 
            ctx.arc(x, y - 5, 28, 0, 2 * math.pi)
            ctx.fill()

            #lingkaran
            ctx.set_source_rgb(0.2, 0.5, 0.15) 
            ctx.arc(x - 12, y - 10, 20, 0, 2 * math.pi)
            ctx.fill()
            ctx.arc(x + 10, y - 15, 22, 0, 2 * math.pi)
            ctx.fill()
            ctx.arc(x + 8, y + 5, 18, 0, 2 * math.pi)
            ctx.fill()
            
            #hilight daun
            ctx.set_source_rgb(0.3, 0.6, 0.2) 
            ctx.arc(x - 5, y - 8, 15, 0, 2 * math.pi)
            ctx.fill()
    
    def draw_lobi(self, ctx):

        # 1. Latar Belakang
        COLOR_MORTAR = (0.3, 0.3, 0.3)
        ctx.set_source_rgb(*COLOR_MORTAR)
        ctx.rectangle(0, 0, screen_width, screen_height)
        ctx.fill()
        
        # 2. Hexagon
        HEX_SIZE = 15 
        GAP = 2
        COLOR_BRICK = (0.5, 0.5, 0.5) 
        ctx.set_source_rgb(*COLOR_BRICK)

        hex_h = HEX_SIZE * 2
        hex_w = math.sqrt(3) * HEX_SIZE
        step_y = (hex_h * 0.75) + (GAP * 0.75) 
        step_x = hex_w + GAP
        num_rows = int(screen_height / step_y) + 2
        num_cols = int(screen_width / step_x) + 2
        y_start = -(GAP / 2)
        x_start = -(GAP / 2)

        for r in range(num_rows):
            y_pos = (r * step_y) + y_start
            offset_x = 0 if r % 2 == 0 else step_x / 2
            
            for c in range(num_cols): 
                x_pos = (c * step_x) + offset_x + x_start
                for i in range(6):
                    angle_rad = (math.pi / 3) * i - (math.pi / 2)
                    vx = x_pos + HEX_SIZE * math.cos(angle_rad)
                    vy = y_pos + HEX_SIZE * math.sin(angle_rad)
                    if i == 0: ctx.move_to(vx, vy)
                    else: ctx.line_to(vx, vy)
                ctx.close_path()
        ctx.fill()
        
        pillar_positions = [
            (300, 300),   
            (900, 300),  
        ]

        PILLAR_SIZE = 60      
        PILLAR_COLOR = (0.7, 0.7, 0.65) 
        SHADOW_OFFSET = 12       
        for (px, py) in pillar_positions:
            
            top_left_x = px - (PILLAR_SIZE / 2)
            top_left_y = py - (PILLAR_SIZE / 2)

            #shadow pilar
            ctx.set_source_rgba(0.0, 0.0, 0.0, 0.3) 
            ctx.rectangle(top_left_x + SHADOW_OFFSET, top_left_y + SHADOW_OFFSET, PILLAR_SIZE, PILLAR_SIZE)
            ctx.fill()

            #pilar
            ctx.set_source_rgb(*PILLAR_COLOR)
            ctx.rectangle(top_left_x, top_left_y, PILLAR_SIZE, PILLAR_SIZE)
            ctx.fill()

            #tepi pilar
            ctx.set_line_width(2)
            ctx.set_source_rgb(0.5, 0.5, 0.45)
            ctx.rectangle(top_left_x, top_left_y, PILLAR_SIZE, PILLAR_SIZE)
            ctx.stroke()
            
            #detail
            DETAIL_SIZE = PILLAR_SIZE * 0.4
            detail_tl_x = px - (DETAIL_SIZE / 2)
            detail_tl_y = py - (DETAIL_SIZE / 2)
            ctx.set_source_rgb(0.8, 0.8, 0.75)
            ctx.rectangle(detail_tl_x, detail_tl_y, DETAIL_SIZE, DETAIL_SIZE)
            ctx.fill()

        kursi_lobi = [
            (100, 100, 90),    
            (400, 100, 90),   
            (700, 100, 90),   
            (500, 300, 0),    
            (700, 300, 0),   
        ]
        
        TABLE_W, TABLE_H = 140, 70
        BENCH_W, BENCH_H = 140, 25
        BENCH_GAP = 5 

        for (fx, fy, rotation_degree) in kursi_lobi:
            ctx.save()
            ctx.translate(fx, fy)
            ctx.rotate(math.radians(rotation_degree))
            ctx.set_source_rgba(0.0, 0.0, 0.0, 0.4) 
            ctx.rectangle(0 - BENCH_W/2 + 5, 0 - TABLE_H/2 - BENCH_GAP - BENCH_H + 5, BENCH_W, BENCH_H)
            ctx.rectangle(0 - TABLE_W/2 + 5, 0 - TABLE_H/2 + 5, TABLE_W, TABLE_H)
            ctx.rectangle(0 - BENCH_W/2 + 5, 0 + TABLE_H/2 + BENCH_GAP + 5, BENCH_W, BENCH_H)
            ctx.fill()

            ctx.set_source_rgb(0.45, 0.30, 0.15) 
            ctx.rectangle(0 - BENCH_W/2, 0 - TABLE_H/2 - BENCH_GAP - BENCH_H, BENCH_W, BENCH_H)
            ctx.rectangle(0 - BENCH_W/2, 0 + TABLE_H/2 + BENCH_GAP, BENCH_W, BENCH_H)
            ctx.fill()

            ctx.set_source_rgb(0.60, 0.40, 0.20) 
            ctx.rectangle(0 - TABLE_W/2, 0 - TABLE_H/2, TABLE_W, TABLE_H)
            ctx.fill()

            ctx.set_source_rgb(0.35, 0.20, 0.10) 
            ctx.set_line_width(2)
            num_planks = 6
            plank_width = TABLE_W / num_planks
            for i in range(1, num_planks):
                line_x = (0 - TABLE_W/2) + (i * plank_width)
                ctx.move_to(line_x, 0 - TABLE_H/2)
                ctx.line_to(line_x, 0 + TABLE_H/2)
            ctx.stroke()
            ctx.restore()
            
    def draw_doubleway(self, ctx):
        
        SIDEWALK_W = 120 
        ROAD_W = 320       

        #paving
        PAVING_SIZE = 20       
        COLOR_PINK_LIGHT = (1.0, 0.7, 0.8) 
        COLOR_PINK_DARK = (0.9, 0.5, 0.6)  

        num_cols = int(screen_width / PAVING_SIZE) + 1
        num_rows = int(screen_height / PAVING_SIZE) + 1

        for c in range(num_cols):
            for r in range(num_rows):
                x = c * PAVING_SIZE
                y = r * PAVING_SIZE

                is_in_sidewalk = (x < SIDEWALK_W) or (x > screen_width - SIDEWALK_W - PAVING_SIZE)

                if is_in_sidewalk:
                    if (c + r) % 2 == 0:
                        ctx.set_source_rgb(*COLOR_PINK_LIGHT)
                    else:
                        ctx.set_source_rgb(*COLOR_PINK_DARK)
                    ctx.rectangle(x, y, PAVING_SIZE, PAVING_SIZE)
                    ctx.fill()

        ctx.set_source_rgb(0.6, 0.3, 0.4) 
        ctx.set_line_width(1)
        for c in range(num_cols + 1):
            ctx.move_to(c * PAVING_SIZE, 0)
            ctx.line_to(c * PAVING_SIZE, screen_height)
        for r in range(num_rows + 1):
            ctx.move_to(0, r * PAVING_SIZE)
            ctx.line_to(screen_width, r * PAVING_SIZE)
        ctx.stroke()

        #taman tengah
        median_x = SIDEWALK_W + ROAD_W
        median_w = screen_width - (2 * (SIDEWALK_W + ROAD_W))

        ctx.set_source_rgb(0.2, 0.6, 0.2) 
        ctx.rectangle(median_x, 0, median_w, screen_height)
        ctx.fill()

        #aspal
        COLOR_ASPHALT = (0.3, 0.3, 0.3) 
        ctx.set_source_rgb(*COLOR_ASPHALT)
        ctx.rectangle(SIDEWALK_W, 0, ROAD_W, screen_height)
        ctx.fill()

        ctx.rectangle(screen_width - SIDEWALK_W - ROAD_W, 0, ROAD_W, screen_height)
        ctx.fill()

        # 4. pembatas
        KERB_SIZE = 15
        num_blocks = 20
        block_h = screen_height / num_blocks

        def draw_kerb_line(x_pos):
            for i in range(num_blocks):
                if i % 2 == 0: ctx.set_source_rgb(0.9, 0.9, 0.9) 
                else: ctx.set_source_rgb(0.0, 0.2, 0.8)          
                ctx.rectangle(x_pos, i * block_h, KERB_SIZE, block_h)
                ctx.fill()

        # Gambar 4 garis pembatas
        draw_kerb_line(SIDEWALK_W - KERB_SIZE)          
        draw_kerb_line(SIDEWALK_W + ROAD_W)             
        draw_kerb_line(screen_width - median_x - KERB_SIZE) 
        draw_kerb_line(screen_width - SIDEWALK_W)        

        #pohon
        center_x = screen_width / 2

        objects_y = [20, 150, 400]
        
        for y in objects_y:


            # wit wit an
            tree_offset_y = 80 
            
            tree_x = center_x
            tree_y = y + tree_offset_y
            
            if tree_y < screen_height + 50: 
                ctx.set_source_rgba(0.0, 0.0, 0.0, 0.3)
                ctx.arc(tree_x + 15, tree_y + 15, 60, 0, 2 * math.pi)
                ctx.fill()

                ctx.set_source_rgb(0.35, 0.2, 0.1)
                ctx.arc(tree_x, tree_y, 10, 0, 2 * math.pi)
                ctx.fill()

                ctx.set_source_rgb(0.1, 0.4, 0.1)
                ctx.arc(tree_x, tree_y, 50, 0, 2 * math.pi)
                ctx.fill()

                ctx.set_source_rgb(0.15, 0.55, 0.15)
                ctx.arc(tree_x - 15, tree_y - 10, 35, 0, 2 * math.pi)
                ctx.fill()
                ctx.arc(tree_x + 15, tree_y + 15, 30, 0, 2 * math.pi)
                ctx.fill()

                ctx.set_source_rgb(0.25, 0.7, 0.25)
                ctx.arc(tree_x - 5, tree_y - 15, 20, 0, 2 * math.pi)
                ctx.fill()
    
    def draw_parkiran(self, ctx):
#paving block
        COLOR_MORTAR = (0.4, 0.4, 0.4)
        ctx.set_source_rgb(*COLOR_MORTAR)
        ctx.rectangle(0, 0, screen_width, screen_height)
        ctx.fill()
        
        PAVING_W = 30   
        PAVING_H = 15 
        GAP = 0.5        
        ctx.set_source_rgb(0.3, 0.3, 0.3) 

        step_x = PAVING_W + GAP
        step_y = PAVING_H + GAP
        
        num_rows = int(screen_height / step_y) + 2
        num_cols = int(screen_width / step_x) + 2

        for r in range(num_rows):
            y_pos = (r * step_y)
            offset_x = -(step_x / 2) if r % 2 == 1 else 0
            
            for c in range(num_cols):
                x_pos = (c * step_x) + offset_x
                ctx.rectangle(x_pos, y_pos, PAVING_W, PAVING_H)
        ctx.fill()
#taman lingkaran
        center_x = screen_width / 2
        center_y = screen_height / 2
        GARDEN_RADIUS = 75      
        KERB_WIDTH = 12         

        ctx.set_source_rgb(0.8, 0.8, 0.8) 
        ctx.arc(center_x, center_y, GARDEN_RADIUS + KERB_WIDTH, 0, 2 * math.pi)
        ctx.fill()
        ctx.set_source_rgb(0.5, 0.5, 0.5) 
        ctx.set_line_width(2)
        ctx.stroke()

        ctx.set_source_rgb(0.2, 0.6, 0.2) 
        ctx.arc(center_x, center_y, GARDEN_RADIUS, 0, 2 * math.pi)
        ctx.fill()

        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.3)
        ctx.arc(center_x + 5, center_y + 5, 30, 0, 2 * math.pi)
        ctx.fill()
        ctx.set_source_rgb(0.1, 0.4, 0.1) 
        ctx.arc(center_x, center_y, 25, 0, 2 * math.pi)
        ctx.fill()
# zone parkir
        ZONE_HEIGHT = 60 
        ROW_GAP = 110
        MARGIN_X = 50
        CORNER_RADIUS = 15
        COLOR_YELLOW_LINE = (0.95, 0.8, 0.1) 

        current_y = 60 
        
        while current_y < screen_height - 60:

            garden_top = center_y - (GARDEN_RADIUS + KERB_WIDTH + 20)
            garden_bottom = center_y + (GARDEN_RADIUS + KERB_WIDTH + 20)
            row_top = current_y
            row_bottom = current_y + ZONE_HEIGHT
            
            is_hitting_garden = (row_bottom > garden_top) and (row_top < garden_bottom)

            zones_to_draw = []
            
            if is_hitting_garden:

                w_left = (center_x - (GARDEN_RADIUS + KERB_WIDTH + 40)) - MARGIN_X
                zones_to_draw.append((MARGIN_X, current_y, w_left, ZONE_HEIGHT))
                
                start_x_right = center_x + (GARDEN_RADIUS + KERB_WIDTH + 40)
                w_right = (screen_width - MARGIN_X) - start_x_right
                zones_to_draw.append((start_x_right, current_y, w_right, ZONE_HEIGHT))
            else:
                full_width = screen_width - (2 * MARGIN_X)
                zones_to_draw.append((MARGIN_X, current_y, full_width, ZONE_HEIGHT))

            for (zx, zy, zw, zh) in zones_to_draw:

                ctx.new_sub_path()
                ctx.arc(zx + zw - CORNER_RADIUS, zy + CORNER_RADIUS, CORNER_RADIUS, -math.pi / 2, 0)
                ctx.arc(zx + zw - CORNER_RADIUS, zy + zh - CORNER_RADIUS, CORNER_RADIUS, 0, math.pi / 2)
                ctx.arc(zx + CORNER_RADIUS, zy + zh - CORNER_RADIUS, CORNER_RADIUS, math.pi / 2, math.pi)
                ctx.arc(zx + CORNER_RADIUS, zy + CORNER_RADIUS, CORNER_RADIUS, math.pi, 3 * math.pi / 2)
                ctx.close_path()

                ctx.set_source_rgba(0.0, 0.0, 0.0, 0.3) 
                ctx.fill_preserve()

                ctx.set_source_rgb(*COLOR_YELLOW_LINE)
                ctx.set_line_width(4)
                ctx.stroke()
            
            current_y += ROW_GAP