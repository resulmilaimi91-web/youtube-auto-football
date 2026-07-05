import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

W = 1280
H = 720


def _get_font(size):
    fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for path in fonts:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _draw_cortana_static(draw, cx, cy, size):
    r = size
    for g in range(5, 0, -1):
        alpha = 40 // g
        draw.ellipse(
            [cx - r - 20 * g, cy - r - 20 * g, cx + r + 20 * g, cy + r + 20 * g],
            fill=(0, 120 + 20 * g, 255, alpha),
        )
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 150, 255))
    draw.ellipse([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5], fill=(50, 180, 255))
    eye_y = cy - int(r * 0.2)
    for eye_x in [cx - int(r * 0.35), cx + int(r * 0.35)]:
        draw.ellipse([eye_x - 7, eye_y - 7, eye_x + 7, eye_y + 7], fill=(255, 255, 255))
        draw.ellipse([eye_x - 3, eye_y - 3, eye_x + 3, eye_y + 3], fill=(0, 50, 100))
    mouth_y = cy + int(r * 0.3)
    draw.arc(
        [cx - int(r * 0.3), mouth_y - int(r * 0.1), cx + int(r * 0.3), mouth_y + 5],
        0, 180, fill=(255, 100, 100), width=4,
    )


def _draw_kid_static(draw, cx, cy, size, shirt_color):
    bounce = 2
    head_r = int(size * 0.25)
    body_h = int(size * 0.35)
    leg_h = int(size * 0.3)
    total_h = head_r * 2 + body_h + leg_h
    head_y = cy - total_h // 2 + head_r + bounce
    draw.ellipse([cx - head_r, head_y - head_r, cx + head_r, head_y + head_r],
                 fill=(255, 210, 160))
    hat_top = head_y - head_r - 8
    draw.polygon([(cx - head_r - 5, hat_top + 15), (cx + head_r + 5, hat_top + 15),
                  (cx + head_r // 2, hat_top)], fill=(255, 50, 50))
    draw.ellipse([cx - head_r - 5, hat_top + 10, cx + head_r + 5, hat_top + 20],
                 fill=(255, 50, 50))
    eye_y2 = head_y - 3
    draw.ellipse([cx - 6, eye_y2 - 4, cx - 1, eye_y2 + 4], fill=(0, 0, 0))
    draw.ellipse([cx + 1, eye_y2 - 4, cx + 6, eye_y2 + 4], fill=(0, 0, 0))
    draw.arc([cx - 8, head_y + 2, cx + 8, head_y + 10], 0, 180, fill=(255, 50, 50), width=2)
    body_top = head_y + head_r + 5 + bounce
    draw.rectangle([cx - 20, body_top, cx + 20, body_top + body_h], fill=shirt_color)
    draw.rectangle([cx - 22, body_top, cx - 15, body_top + 10], fill=(255, 255, 255))
    draw.rectangle([cx + 15, body_top, cx + 22, body_top + 10], fill=(255, 255, 255))
    arm_swing = 3
    draw.rectangle([cx - 30, body_top + 5 + arm_swing, cx - 22, body_top + body_h // 2 + arm_swing],
                   fill=shirt_color)
    draw.rectangle([cx + 22, body_top + 5 - arm_swing, cx + 30, body_top + body_h // 2 - arm_swing],
                   fill=shirt_color)
    leg_top = body_top + body_h
    draw.rectangle([cx - 15, leg_top, cx - 3, leg_top + leg_h], fill=(80, 120, 200))
    draw.rectangle([cx + 3, leg_top, cx + 15, leg_top + leg_h], fill=(80, 120, 200))
    return head_y


def generate_thumbnail(title, theme, output_path):
    img = Image.new("RGBA", (W, H), (20, 30, 60))
    draw = ImageDraw.Draw(img)

    bg_shapes = [
        (random.randint(0, W), random.randint(0, H // 2), random.randint(30, 80))
        for _ in range(8)
    ]
    for bx, by, br in bg_shapes:
        c = random.choice([(255, 215, 0, 40), (255, 100, 100, 30), (100, 200, 255, 35)])
        draw.ellipse([bx - br, by - br, bx + br, by + br], fill=c)

    wave_y = H - 60
    for x in range(0, W, 4):
        wy = wave_y + int(15 * math.sin(x * 0.02))
        draw.line([(x, wy), (x, H)], fill=(50, 180, 100, 60))

    _draw_cortana_static(draw, W // 2 - 220, H // 2 - 10, 90)
    _draw_kid_static(draw, W // 2 + 180, H // 2 + 30, 140, (255, 200, 100))
    _draw_kid_static(draw, W // 2 + 50, H // 2 + 40, 120, (100, 200, 255))

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([(0, H - 160), (W, H)], fill=(0, 0, 0, 180))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    font_large = _get_font(48)
    words = title.split()
    lines = []
    current = ""
    for w in words:
        test = (current + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font_large)
        if bbox[2] - bbox[0] > W - 100:
            lines.append(current)
            current = w
        else:
            current = test
    lines.append(current)

    y_offset = H - 140
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_large)
        tw = bbox[2] - bbox[0]
        draw.rectangle(
            [(W - tw) // 2 - 15, y_offset - 5, (W + tw) // 2 + 15, y_offset + 55],
            fill=(255, 50, 50, 220),
        )
        draw.rectangle(
            [(W - tw) // 2 - 15, y_offset - 5, (W + tw) // 2 + 15, y_offset + 55],
            fill=None, outline=(255, 200, 50), width=3,
        )
        draw.text(((W - tw) // 2, y_offset), line, fill=(255, 255, 255), font=font_large)
        y_offset += 55

    font_sub = _get_font(28)
    sub_text = "Sing Along & Learn!"
    sb = draw.textbbox((0, 0), sub_text, font=font_sub)
    sw = sb[2] - sb[0]
    draw.text(((W - sw) // 2, 20), sub_text, fill=(255, 215, 0), font=font_sub)

    for star_x in range(50, W, 100):
        sy = 40 + 20 * math.sin(star_x * 0.05)
        draw.text((star_x, sy), "★", fill=(255, 215, 0, 100), font=_get_font(20))
        draw.text((star_x + 50, sy + 15), "★", fill=(255, 215, 0, 80), font=_get_font(14))

    img = img.convert("RGB")
    img.save(output_path, quality=95)


def generate_short_thumbnail(title, theme, output_path, is_vertical=True):
    w, h = (1080, 1920) if is_vertical else (1280, 720)
    img = Image.new("RGBA", (w, h), (20, 30, 60))
    draw = ImageDraw.Draw(img)

    for _ in range(10):
        bx = random.randint(0, w)
        by = random.randint(0, h)
        br = random.randint(40, 120)
        c = random.choice([(255, 215, 0, 30), (255, 100, 100, 25), (100, 200, 255, 30)])
        draw.ellipse([bx - br, by - br, bx + br, by + br], fill=c)

    cx = w // 2
    cy = h // 2 - 100
    _draw_cortana_static(draw, cx - 100, cy, 60)
    _draw_kid_static(draw, cx + 120, cy + 50, 100, (255, 200, 100))
    _draw_kid_static(draw, cx + 20, cy + 60, 80, (100, 200, 255))

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([(0, h - 200), (w, h)], fill=(0, 0, 0, 180))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    font_large = _get_font(40)
    words = title.split()
    lines = []
    current = ""
    for wd in words:
        test = (current + " " + wd).strip()
        bbox = draw.textbbox((0, 0), test, font=font_large)
        if bbox[2] - bbox[0] > w - 80:
            lines.append(current)
            current = wd
        else:
            current = test
    lines.append(current)

    y_offset = h - 170
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_large)
        tw = bbox[2] - bbox[0]
        draw.rectangle(
            [(w - tw) // 2 - 15, y_offset - 5, (w + tw) // 2 + 15, y_offset + 48],
            fill=(255, 50, 50, 220),
        )
        draw.text(((w - tw) // 2, y_offset), line, fill=(255, 255, 255), font=font_large)
        y_offset += 48

    font_sub = _get_font(22)
    sub_text = "★ Kids Songs & Learning ★"
    sb = draw.textbbox((0, 0), sub_text, font=font_sub)
    sw = sb[2] - sb[0]
    draw.text(((w - sw) // 2, 30), sub_text, fill=(255, 215, 0), font=font_sub)

    img = img.convert("RGB")
    img.save(output_path, quality=95)
