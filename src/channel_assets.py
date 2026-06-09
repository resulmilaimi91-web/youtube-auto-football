import os
import math
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)


def _get_font(size):
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "arial.ttf",
    ]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _draw_radial_gradient(draw, W, H, c1, c2):
    for y in range(H):
        for x in range(W):
            dx = (x - W / 2) / (W / 2)
            dy = (y - H / 2) / (H / 2)
            dist = min(math.sqrt(dx * dx + dy * dy), 1.0)
            r = int(c1[0] + (c2[0] - c1[0]) * dist)
            g = int(c1[1] + (c2[1] - c1[1]) * dist)
            b = int(c1[2] + (c2[2] - c1[2]) * dist)
            draw.point((x, y), fill=(r, g, b))


def create_logo(output_path):
    W, H = 800, 800
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, H], fill=(10, 15, 35))

    for r in range(350, 0, -1):
        ratio = r / 350
        cr = int(0 + (0 - 0) * ratio)
        cg = int(50 + (120 - 50) * ratio)
        cb = int(120 + (220 - 120) * ratio)
        draw.ellipse([W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r], fill=(cr, cg, cb))

    for r in range(300, 0, -1):
        ratio = r / 300
        cr = int(0 + (10 - 0) * ratio)
        cg = int(30 + (15 - 30) * ratio)
        cb = int(80 + (35 - 80) * ratio)
        draw.ellipse([W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r], fill=(cr, cg, cb))

    draw.ellipse([W // 2 - 200, H // 2 - 200, W // 2 + 200, H // 2 + 200], fill=(0, 50, 120))
    draw.ellipse([W // 2 - 180, H // 2 - 180, W // 2 + 180, H // 2 + 180], outline=(255, 215, 0), width=6)

    font_huge = _get_font(140)
    font_med = _get_font(60)

    bbox = draw.textbbox((0, 0), "WC", font=font_huge)
    tw = bbox[2] - bbox[0]
    draw.text((W // 2 - tw // 2, H // 2 - 100), "WC", fill=(255, 215, 0), font=font_huge)

    bbox2 = draw.textbbox((0, 0), "2026", font=font_med)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((W // 2 - tw2 // 2, H // 2 + 50), "2026", fill="white", font=font_med)

    for i in range(4):
        draw.line([(W // 2 - 160 + i * 2, H // 2 + 30), (W // 2 + 160 - i * 2, H // 2 + 30)],
                  fill=(255, 215, 0), width=2)

    draw.rectangle([0, 0, W, 8], fill=(255, 215, 0))
    draw.rectangle([0, H - 8, W, H], fill=(255, 215, 0))
    draw.rectangle([0, 0, 8, H], fill=(255, 215, 0))
    draw.rectangle([W - 8, 0, W, H], fill=(255, 215, 0))

    img.save(output_path, quality=95)
    print(f"  Logo saved: {output_path}")
    return output_path


def create_banner(output_path):
    W, H = 2560, 1440
    img = Image.new("RGB", (W, H), (10, 15, 35))
    draw = ImageDraw.Draw(img)

    for y in range(H):
        ratio = y / H
        r = int(10 + (5 - 10) * ratio)
        g = int(15 + (25 - 15) * ratio)
        b = int(35 + (60 - 35) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    draw.rectangle([0, 0, W, 120], fill=(0, 50, 120))
    draw.rectangle([0, H - 120, W, H], fill=(0, 50, 120))

    for i in range(3):
        draw.line([(0, 120 + i), (W, 120 + i)], fill=(255, 215, 0), width=2)
        draw.line([(0, H - 123 + i), (W, H - 123 + i)], fill=(255, 215, 0), width=2)

    font_huge = _get_font(120)
    font_big = _get_font(80)
    font_med = _get_font(50)

    title = "FOOTBALL HIGHLIGHTS DAILY"
    bbox = draw.textbbox((0, 0), title, font=font_huge)
    tw = bbox[2] - bbox[0]
    draw.text((W // 2 - tw // 2 + 4, 204), title, fill=(0, 0, 0), font=font_huge)
    draw.text((W // 2 - tw // 2, 200), title, fill="white", font=font_huge)

    subtitle = "FIFA WORLD CUP 2026  |  DAILY NEWS  |  HIGHLIGHTS  |  ANALYSIS"
    bbox2 = draw.textbbox((0, 0), subtitle, font=font_med)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((W // 2 - tw2 // 2, 380), subtitle, fill=(255, 215, 0), font=font_med)

    cities = ["ATLANTA", "BOSTON", "DALLAS", "GUADALAJARA", "HOUSTON", "KANSAS CITY",
              "LOS ANGELES", "MEXICO CITY", "MIAMI", "MONTERREY", "NEW YORK",
              "PHILADELPHIA", "SAN FRANCISCO", "SEATTLE", "TORONTO", "VANCOUVER"]
    font_small = _get_font(36)
    x_pos = 100
    for city in cities:
        draw.text((x_pos, 500), city, fill=(180, 200, 220), font=font_small)
        x_pos += 150
        if x_pos > W - 200:
            x_pos = 100

    countries = ["USA", "MEXICO", "CANADA"]
    for i, country in enumerate(countries):
        cx = W // 4 * (i + 1)
        draw.ellipse([cx - 60, 620, cx + 60, 740], fill=(0, 50, 120), outline=(255, 215, 0), width=3)
        bbox_c = draw.textbbox((0, 0), country, font=font_med)
        tw_c = bbox_c[2] - bbox_c[0]
        draw.text((cx - tw_c // 2, 650), country, fill="white", font=font_med)

    stats = ["48 TEAMS", "16 VENUES", "104 MATCHES", "39 DAYS"]
    for i, stat in enumerate(stats):
        sx = 200 + i * 580
        draw.rectangle([sx, 820, sx + 500, 920], fill=(255, 215, 0, 50), outline=(255, 215, 0), width=2)
        bbox_s = draw.textbbox((0, 0), stat, font=font_big)
        tw_s = bbox_s[2] - bbox_s[0]
        draw.text((sx + 250 - tw_s // 2, 840), stat, fill="white", font=font_big)

    draw.text((W // 2 - 200, 1000), "SUBSCRIBE NOW", fill=(255, 215, 0), font=font_huge)

    img.save(output_path, quality=95)
    print(f"  Banner saved: {output_path}")
    return output_path


def create_profile_pic(output_path):
    W, H = 800, 800
    img = Image.new("RGB", (W, H), (0, 50, 120))
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, H], fill=(0, 50, 120))

    for r in range(380, 0, -1):
        ratio = r / 380
        cr = int(0 + (10 - 0) * ratio)
        cg = int(50 + (15 - 50) * ratio)
        cb = int(120 + (35 - 120) * ratio)
        draw.ellipse([W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r], fill=(cr, cg, cb))

    draw.ellipse([W // 2 - 300, H // 2 - 300, W // 2 + 300, H // 2 + 300], fill=(0, 40, 100))
    draw.ellipse([W // 2 - 280, H // 2 - 280, W // 2 + 280, H // 2 + 280], outline=(255, 215, 0), width=8)

    font_huge = _get_font(180)
    font_big = _get_font(100)

    bbox = draw.textbbox((0, 0), "FH", font=font_huge)
    tw = bbox[2] - bbox[0]
    draw.text((W // 2 - tw // 2, H // 2 - 130), "FH", fill=(255, 215, 0), font=font_huge)

    bbox2 = draw.textbbox((0, 0), "2026", font=font_big)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((W // 2 - tw2 // 2, H // 2 + 60), "2026", fill="white", font=font_big)

    draw.rectangle([0, 0, W, 10], fill=(255, 215, 0))
    draw.rectangle([0, H - 10, W, H], fill=(255, 215, 0))
    draw.rectangle([0, 0, 10, H], fill=(255, 215, 0))
    draw.rectangle([W - 10, 0, W, H], fill=(255, 215, 0))

    img.save(output_path, quality=95)
    print(f"  Profile pic saved: {output_path}")
    return output_path


if __name__ == "__main__":
    create_logo(os.path.join(ASSETS_DIR, "channel_logo.png"))
    create_banner(os.path.join(ASSETS_DIR, "channel_banner.png"))
    create_profile_pic(os.path.join(ASSETS_DIR, "channel_profile.png"))
    print("All channel assets created!")
