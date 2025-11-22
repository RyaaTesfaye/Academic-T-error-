import cairo
from operator import itemgetter
from lib.functions.drawTextCenter import draw_text_centered
from lib.functions.hexToRGB import hex_to_rgb
from lib.functions.rounded import rounded_rect

def scoreBoard(ctx, scores, x, y, is_minimized=False):
    ctx.save()
    ctx.translate(x, y)

    rank_colors = ["#FFD700", "#C0C0C0", "#CD7F32", "#F78310", "#FFFFFF"]
    sorted_data = sorted(scores.items(), key=itemgetter(1), reverse=True)
    
    user_data = None
    processed_scores = []
    
    for idx, (name, val) in enumerate(sorted_data):
        is_me = (name.lower() == "you")
        
        if is_me:
            u_color = rank_colors[idx] if idx < 3 else "#FFFFFF"
            user_data = {
                "rank": str(idx + 1),
                "name": name,
                "score": str(val),
                "color": u_color
            }

        if idx < 5:
            color = rank_colors[idx] if idx < 3 else "#FFFFFF"
            processed_scores.append({
                "rank": str(idx + 1),
                "name": name,
                "score": str(val),
                "color": color,
                "highlight": is_me
            })


    if is_minimized:
        if user_data:
            mini_w, mini_h = 240, 60 
            
            rounded_rect(ctx, 0, 10, mini_w, mini_h, 15)
            ctx.set_source_rgba(*hex_to_rgb("#8B5A2B", 0.4))
            ctx.fill_preserve()
            ctx.set_line_width(2)
            ctx.set_source_rgba(*hex_to_rgb("#3E2723"))
            ctx.stroke()
            
            slot_x, slot_y = 10, 20
            slot_w = mini_w - 20
            slot_h = 30
            
            rounded_rect(ctx, slot_x, slot_y, slot_w, slot_h, 6)
            ctx.set_source_rgba(*hex_to_rgb("#5D3A1A", 0.9))
            ctx.fill_preserve()
            ctx.set_source_rgba(*hex_to_rgb("#FF8C00"))
            ctx.stroke()

            fs = 12
            y_off = 20 
            ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            ctx.set_font_size(fs)

            ctx.set_source_rgba(*hex_to_rgb(user_data["color"]))
            ctx.move_to(slot_x + 10, slot_y + y_off)
            ctx.show_text(user_data["rank"] + ".")

            ctx.set_source_rgba(1, 1, 1, 1)
            ctx.move_to(slot_x + 35, slot_y + y_off)
            ctx.show_text(user_data["name"])

            score_extents = ctx.text_extents(user_data["score"])
            ctx.set_source_rgba(*hex_to_rgb(user_data["color"]))
            ctx.move_to(slot_x + slot_w - score_extents.width - 10, slot_y + y_off)
            ctx.show_text(user_data["score"])

        else:
            draw_text_centered(ctx, "User not found", 120, 25, 12, cairo.FONT_WEIGHT_BOLD, (1,1,1))

    else:
        WIDTH, HEIGHT = 240, 240
        board_x, board_y = 10, 10
        board_w, board_h = WIDTH - 20, HEIGHT - 20
        corner_radius = 20

        ctx.save()
        rounded_rect(ctx, board_x + 3, board_y + 5, board_w, board_h, corner_radius)
        ctx.set_source_rgba(0, 0, 0, 0.4)
        ctx.fill()
        ctx.restore()

        rounded_rect(ctx, board_x, board_y, board_w, board_h, corner_radius)
        ctx.set_source_rgba(*hex_to_rgb("#8B5A2B", 0.4))
        ctx.fill_preserve()

        ctx.save()
        ctx.clip()
        ctx.set_source_rgba(0, 0, 0, 0.05)
        ctx.set_line_width(2)
        for i in range(-HEIGHT, WIDTH + HEIGHT, 15):
            ctx.move_to(i, 0)
            ctx.line_to(i + HEIGHT, HEIGHT)
        ctx.stroke()
        ctx.restore()

        rounded_rect(ctx, board_x, board_y, board_w, board_h, corner_radius)
        ctx.set_line_width(5)
        ctx.set_source_rgba(*hex_to_rgb("#3E2723"))
        ctx.stroke_preserve()
        ctx.set_line_width(2)
        ctx.set_source_rgba(*hex_to_rgb("#5D3A1A"))
        ctx.stroke()

        draw_text_centered(ctx, "AKADEMIA T(ERROR)", WIDTH/2, board_y + 30, 13, cairo.FONT_WEIGHT_BOLD, hex_to_rgb("#FFD700"), "Serif")

        label_w, label_h = 100, 20
        label_x = (WIDTH - label_w) / 2
        label_y = board_y + 45

        rounded_rect(ctx, label_x, label_y, label_w, label_h, 5)
        ctx.set_source_rgba(*hex_to_rgb("#3E2723", 0.9))
        ctx.fill()
        draw_text_centered(ctx, "LIST SCORE", WIDTH/2, label_y + 14, 10, cairo.FONT_WEIGHT_BOLD, hex_to_rgb("#FFFFFF"))

        start_y = label_y + 28
        slot_h = 22
        slot_w = board_w - 30
        slot_x = board_x + 15
        gap = 3

        for i, data in enumerate(processed_scores):
            current_y = start_y + i * (slot_h + gap)

            rounded_rect(ctx, slot_x, current_y, slot_w, slot_h, 6)

            if data.get("highlight"):
                ctx.set_source_rgba(*hex_to_rgb("#5D3A1A", 0.9))
                ctx.fill_preserve()
                ctx.set_source_rgba(*hex_to_rgb("#FF8C00"))
                ctx.set_line_width(2)
                ctx.stroke()
            else:
                ctx.set_source_rgba(0, 0, 0, 0.2)
                ctx.fill()

            fs = 11
            y_off = 16

            ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            ctx.set_font_size(fs)

            ctx.set_source_rgba(*hex_to_rgb(data["color"]))
            ctx.move_to(slot_x + 10, current_y + y_off)
            ctx.show_text(data["rank"] + ".")

            ctx.set_source_rgba(*hex_to_rgb("#FFE4B5"))
            if data.get("highlight"):
                ctx.set_source_rgba(1, 1, 1, 1)
            
            ctx.move_to(slot_x + 30, current_y + y_off)
            ctx.show_text(data["name"])

            score_text = data["score"]
            score_extents = ctx.text_extents(score_text)
            ctx.set_source_rgba(*hex_to_rgb(data["color"]))
            ctx.move_to(slot_x + slot_w - score_extents.width - 10, current_y + y_off)
            ctx.show_text(score_text)

    ctx.restore()