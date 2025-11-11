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

