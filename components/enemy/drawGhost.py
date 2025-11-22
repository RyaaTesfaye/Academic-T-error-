def draw_ghost(ctx, center_x, center_y, pixel_size, image, flip_horizontal=False):
    pixel_height = len(image)
    pixel_width = len(image[0])
    
    total_draw_width = pixel_width * pixel_size
    total_draw_height = pixel_height * pixel_size
    
    start_x = center_x - (total_draw_width / 2)
    start_y = center_y - (total_draw_height / 2)

    for y, row in enumerate(image):
        for x, pixel_color_code in enumerate(row):
            
            if pixel_color_code == 0:
                continue  
            elif pixel_color_code == 1:
                ctx.set_source_rgba(0.0, 0.0, 0.0, 1.0) 
            elif pixel_color_code == 2:
                ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
            elif pixel_color_code == 3:
                ctx.set_source_rgba(0.27, 0.27, 0.27, 1.00) 
            elif pixel_color_code == 4:
                ctx.set_source_rgba(0.50, 0.57, 0.66, 1.00)
            elif pixel_color_code == 5:
                ctx.set_source_rgba(0.44, 0.60, 0.82, 1.00)
            else:
                ctx.set_source_rgba(0.33, 0.43, 0.56, 1.00)

            if flip_horizontal:
                draw_x = (pixel_width - 1) - x
            else:
                draw_x = x
            
            px = start_x + (draw_x * pixel_size)
            py = start_y + (y * pixel_size)
            
            ctx.rectangle(px, py, pixel_size * 1.01, pixel_size * 1.01)
            ctx.fill()