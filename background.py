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
        # --- 1. LAYER DASAR (Warna Nat/Semen) ---
        ctx.set_source_rgb(0.78, 0.78, 0.78) 
        ctx.rectangle(0, 0, screen_width, screen_height)
        ctx.fill()
        
        # --- 2. POLA PAVING BLOCK (Persegi Panjang) ---
        PAVING_W = 5   
        PAVING_H = 3  
        GAP = 0.5        
        
        # Warna balok 
        ctx.set_source_rgb(0.65, 0.65, 0.65) 

        step_x = PAVING_W + GAP
        step_y = PAVING_H + GAP
        
        #jumlah baris dan kolom
        num_rows = int(screen_height / step_y) + 2
        num_cols = int(screen_width / step_x) + 2

        #Grid Paving
        for r in range(num_rows):
            y_pos = (r * step_y)
            
            #Geser baris ganjil
            offset_x = 0
            if r % 2 == 1:
                offset_x = -(step_x / 2)
            
            for c in range(num_cols):
                x_pos = (c * step_x) + offset_x
                # Tambahkan path persegi panjang
                ctx.rectangle(x_pos, y_pos, PAVING_W, PAVING_H)
        
        # Isi warnanya sekaligus (Optimisasi)
        ctx.fill()

        #LAPANGAN HIJAU 
        w, h = 1100, 500
        x_field = (screen_width - w) / 2
        y_field = (screen_height - h) / 2

        ctx.set_source_rgb(0, 0.5, 0)
        ctx.rectangle(x_field, y_field, w, h)
        ctx.fill()
        
        KERB_THICKNESS = 8 
        SEGMENT_LEN = 40   
        
        #garis putih
        ctx.set_line_width(KERB_THICKNESS)
        ctx.set_source_rgb(0.9, 0.9, 0.9)
        ctx.rectangle(x_field, y_field, w, h)
        ctx.stroke()
        
        #garis BIRU
        ctx.set_source_rgb(0.0, 0.2, 0.8) 
        # Pola dash: [Panjang garis, Panjang spasi]
        ctx.set_dash([SEGMENT_LEN, SEGMENT_LEN], 0) 
        ctx.rectangle(x_field, y_field, w, h)
        ctx.stroke()
        
        #RESET DASH 
        ctx.set_dash([], 0)

        # --- 4. HIASAN LAPANGAN (Kuning) ---
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

        # --- 5. POHON ---
        tree_positions = [
            (100, 100),  
            (100, 300), 
            (100, 500),
            (1000, 100),
            (1000, 300),
            (1000, 500),    
        ]

        for (x, y) in tree_positions:
            # 1. Gambar Bayangan (Shadow)
            ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
            ctx.arc(x + 10, y + 10, 30, 0, 2 * math.pi)
            ctx.fill()

            # 2. Gambar Batang (Trunk)
            ctx.set_source_rgb(0.4, 0.2, 0.1) 
            ctx.arc(x, y, 6, 0, 2 * math.pi)
            ctx.fill()

            # 3. Gambar Kanopi (Canopy / Daun)
            ctx.set_source_rgb(0.1, 0.4, 0.1) 
            ctx.arc(x, y - 5, 28, 0, 2 * math.pi)
            ctx.fill()

            # Tumpukan lingkaran yang lebih kecil dan lebih terang
            ctx.set_source_rgb(0.2, 0.5, 0.15) 
            ctx.arc(x - 12, y - 10, 20, 0, 2 * math.pi)
            ctx.fill()
            ctx.arc(x + 10, y - 15, 22, 0, 2 * math.pi)
            ctx.fill()
            ctx.arc(x + 8, y + 5, 18, 0, 2 * math.pi)
            ctx.fill()
            
            # Tumpukan highlight (paling kecil, paling terang)
            ctx.set_source_rgb(0.3, 0.6, 0.2) 
            ctx.arc(x - 5, y - 8, 15, 0, 2 * math.pi)
            ctx.fill()
    
    def draw_lobi(self, ctx):
        # --- 1. Latar Belakang (Nat/Semen) ---
        COLOR_MORTAR = (0.8, 0.8, 0.8)
        ctx.set_source_rgb(*COLOR_MORTAR)
        ctx.rectangle(0, 0, screen_width, screen_height)
        ctx.fill()
        
        # --- 2. Balok Paving Segi Enam ---
        HEX_SIZE = 15 
        GAP = 6

        COLOR_BRICK = (0.9, 0.9, 0.9) 
        
        ctx.set_source_rgb(*COLOR_BRICK)

        hex_h = HEX_SIZE * 2
        hex_w = math.sqrt(3) * HEX_SIZE
        
        step_y = (hex_h * 0.75) + (GAP * 0.75) 
        step_x = hex_w + GAP

        num_rows = int(screen_height / step_y) + 2
        num_cols = int(screen_width / step_x) + 2
        
        y_start = -(GAP / 2)
        x_start = -(GAP / 2)

        # Mulai membangun path
        for r in range(num_rows):
            y_pos = (r * step_y) + y_start
            
            offset_x = 0
            if r % 2 == 1:
                offset_x = step_x / 2
            
            for c in range(num_cols): 
                x_pos = (c * step_x) + offset_x + x_start
                
                # --- LOGIKA draw_hexagon DI-INLINE DI SINI ---
                for i in range(6):
                    angle_rad = (math.pi / 3) * i - (math.pi / 2)
                    
                    vx = x_pos + HEX_SIZE * math.cos(angle_rad)
                    vy = y_pos + HEX_SIZE * math.sin(angle_rad)
                    
                    if i == 0:
                        ctx.move_to(vx, vy)
                    else:
                        ctx.line_to(vx, vy)
                
                ctx.close_path()
                ctx.fill()