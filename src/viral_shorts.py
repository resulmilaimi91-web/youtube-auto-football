import os
import random
import urllib.request
import math
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from moviepy import (
    ImageClip, AudioFileClip, concatenate_videoclips,
)
from moviepy.audio.fx import AudioFadeIn, AudioFadeOut
from src.config import Config


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


def _draw_star(draw, cx, cy, size, fill):
    points = []
    for i in range(5):
        angle = math.radians(-90 + i * 72)
        points.append((cx + size * math.cos(angle), cy + size * math.sin(angle)))
        angle2 = math.radians(-90 + i * 72 + 36)
        points.append((cx + size * 0.4 * math.cos(angle2), cy + size * 0.4 * math.sin(angle2)))
    draw.polygon(points, fill=fill)


def _create_cartoon_bg(theme_idx):
    W, H = 1080, 1920

    palettes = [
        {"sky_top": (100, 180, 255), "sky_bot": (200, 230, 255), "ground": (50, 200, 100), "accent": (255, 220, 50)},
        {"sky_top": (255, 150, 100), "sky_bot": (255, 200, 150), "ground": (150, 100, 200), "accent": (255, 255, 100)},
        {"sky_top": (180, 100, 255), "sky_bot": (220, 180, 255), "ground": (50, 200, 150), "accent": (255, 200, 50)},
        {"sky_top": (50, 200, 200), "sky_bot": (150, 230, 230), "ground": (100, 220, 100), "accent": (255, 255, 150)},
    ]
    pal = palettes[theme_idx % len(palettes)]

    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    for y in range(H):
        ratio = y / H
        r = int(pal["sky_top"][0] + (pal["sky_bot"][0] - pal["sky_top"][0]) * ratio)
        g = int(pal["sky_top"][1] + (pal["sky_bot"][1] - pal["sky_top"][1]) * ratio)
        b = int(pal["sky_top"][2] + (pal["sky_bot"][2] - pal["sky_top"][2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    ground_y = int(H * 0.75)
    draw.rectangle([0, ground_y, W, H], fill=pal["ground"])
    draw.rectangle([0, ground_y - 10, W, ground_y], fill=(pal["ground"][0] + 30, pal["ground"][1] + 30, pal["ground"][2] + 30))

    for i in range(6):
        cx = random.randint(100, W - 100)
        cy = random.randint(80, ground_y - 200)
        size = random.randint(40, 100)
        alpha = random.randint(60, 150)
        draw.ellipse([cx - size, cy - size // 2, cx + size, cy + size // 2], fill=(255, 255, 255, alpha))

    for i in range(5):
        cx = random.randint(50, W - 50)
        cy = random.randint(50, ground_y - 300)
        size = random.randint(20, 40)
        _draw_star(draw, cx, cy, size, pal["accent"] + (random.randint(100, 200),))

    for i in range(8):
        cx = random.randint(100, W - 100)
        cy = random.randint(ground_y + 20, H - 50)
        rsize = random.randint(30, 80)
        colors = [(255, 100, 100), (255, 255, 100), (100, 255, 100), (255, 150, 200), (100, 200, 255)]
        draw.ellipse([cx - rsize, cy - rsize // 2, cx + rsize, cy + rsize // 2], fill=random.choice(colors))

    if random.random() > 0.5:
        for i in range(3):
            cx = random.randint(200, W - 200)
            cy = random.randint(ground_y - 30, ground_y + 30)
            draw.ellipse([cx - 60, cy - 40, cx + 60, cy + 40], fill=(100, 180, 80))
            draw.ellipse([cx - 50, cy - 50, cx + 50, cy + 50], fill=(80, 160, 60))
            draw.ellipse([cx - 10, cy - 15, cx + 10, cy + 5], fill=(255, 200, 100))

    return img


KIDS_FACTS = [
    {
        "title": "Did You Know? Octopus has 3 hearts! #shorts #kids #funfacts",
        "script": "Did you know an octopus has three hearts? Two pump blood to the gills, one pumps it to the body. And when they swim, the heart that pumps to the body stops! That's why they prefer to crawl. Amazing, right?",
        "text": (255, 255, 255),
        "accent": (255, 215, 0),
        "hooks": ["WAIT, WHAT?!", "MIND-BLOWING!", "NO WAY!"],
    },
    {
        "title": "Space Fact: Stars are GIANT! #shorts #kids #space",
        "script": "Did you know the biggest star in the universe is called UY Scuti? It is so huge that if it were our sun, it would swallow everything up to the planet Saturn! Our sun is tiny compared to it!",
        "text": (255, 255, 255),
        "accent": (255, 200, 50),
        "hooks": ["STOP SCROLLING!", "THAT'S HUGE!", "INCREDIBLE!"],
    },
    {
        "title": "Honey never spoils! #shorts #kids #nature",
        "script": "Did you know honey never goes bad? Archaeologists found 3000-year-old honey in Egyptian tombs and it was still perfectly good to eat! Honey is the only food that lasts forever!",
        "text": (255, 255, 255),
        "accent": (255, 215, 0),
        "hooks": ["AMAZING!", "THAT'S OLD!", "WOW!"],
    },
    {
        "title": "Bananas are berries, but strawberries aren't! #shorts #kids",
        "script": "Did you know bananas are technically berries, but strawberries are NOT? A berry has seeds inside, not outside. So bananas qualify, but strawberries don't! Science is so weird!",
        "text": (255, 255, 255),
        "accent": (255, 100, 100),
        "hooks": ["WHAT?!", "THAT'S CRAZY!", "NO WAY!"],
    },
    {
        "title": "Butterflies taste with their feet! #shorts #kids #animals",
        "script": "Did you know butterflies taste food with their feet? They have taste sensors on their legs! When they land on a flower, they taste it immediately. Cool, right?",
        "text": (255, 255, 255),
        "accent": (255, 100, 200),
        "hooks": ["REALLY?!", "THAT'S WILD!", "AMAZING!"],
    },
    {
        "title": "The Sun is 400 times bigger! #shorts #kids #science",
        "script": "Did you know the Sun is 400 times bigger than the Moon? But it also is 400 times farther away. That's why they look the same size in the sky! Perfect cosmic coincidence!",
        "text": (255, 255, 255),
        "accent": (255, 255, 100),
        "hooks": ["COSMIC!", "WOW!", "INCREDIBLE!"],
    },
]


def _create_kids_frame(W, H, theme, hook_text, bg_image, part=0):
    img = bg_image.copy()
    img = img.resize((W, H), Image.LANCZOS)

    draw = ImageDraw.Draw(img)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)

    ov_draw.rectangle([0, 80, W, 550], fill=(0, 0, 0, 140))
    ov_draw.rectangle([0, H - 320, W, H - 80], fill=(0, 0, 0, 140))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    font_huge = _get_font(100)
    font_hook = _get_font(70)
    font_big = _get_font(55)
    font_title = _get_font(50)

    hook_y = 40
    bbox = draw.textbbox((0, 0), hook_text, font=font_hook)
    tw = bbox[2] - bbox[0]
    draw.text((W // 2 - tw // 2 + 3, hook_y + 3), hook_text, fill=(0, 0, 0), font=font_hook)
    draw.text((W // 2 - tw // 2, hook_y), hook_text, fill=theme["accent"], font=font_hook)

    cx, cy = W // 2, H // 2 + 30
    draw.ellipse([cx - 130, cy - 130, cx + 130, cy + 130], fill=(0, 0, 0, 180))
    draw.ellipse([cx - 125, cy - 125, cx + 125, cy + 125], outline=theme["accent"], width=5)

    play_x = cx - 45
    play_y = cy - 60
    draw.polygon([(play_x, play_y), (play_x, play_y + 120), (play_x + 100, play_y + 60)], fill=theme["accent"])

    title_words = theme["title"].split("#")[0].strip()
    if title_words:
        bbox_t = draw.textbbox((0, 0), title_words[:40], font=font_title)
        tw_t = bbox_t[2] - bbox_t[0]
        y_t = min(H // 2 - 200, 600)
        draw.text((W // 2 - tw_t // 2, y_t), title_words[:40], fill=theme["accent"], font=font_title)

    draw.rectangle([60, H - 260, W - 60, H - 140], fill=(255, 50, 50))
    bbox_sub = draw.textbbox((0, 0), "SUBSCRIBE FOR FUN!", font=font_big)
    tw_sub = bbox_sub[2] - bbox_sub[0]
    draw.text((W // 2 - tw_sub // 2, H - 245), "SUBSCRIBE FOR FUN!", fill=(255, 255, 255), font=font_big)

    draw.rectangle([0, 0, W, 8], fill=theme["accent"])
    draw.rectangle([0, H - 8, W, H], fill=theme["accent"])

    for i in range(3):
        sy = 600 + i * 50
        sx = random.randint(50, W - 50)
        _draw_star(draw, sx, sy, 15, theme["accent"])

    return img


def create_kids_short(theme_idx, output_path, voice_path=None):
    theme = KIDS_FACTS[theme_idx % len(KIDS_FACTS)]
    W, H = 1080, 1920
    part_duration = 4

    bg_image = _create_cartoon_bg(theme_idx)

    frames = []
    for part in range(2):
        hook = theme["hooks"][part % len(theme["hooks"])]
        frame = _create_kids_frame(W, H, theme, hook, bg_image, part)
        frame_path = output_path.replace(".mp4", f"_part{part}.png")
        frame.save(frame_path, quality=95)
        frames.append(frame_path)

    clips = []
    for i, frame_path in enumerate(frames):
        clip = ImageClip(frame_path, duration=part_duration)
        clip = clip.with_effects([AudioFadeIn(0.3), AudioFadeOut(0.3)])
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")

    if voice_path and os.path.exists(voice_path) and os.path.getsize(voice_path) > 1000:
        audio = AudioFileClip(voice_path)
        video = video.with_audio(audio)

    video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        preset="fast",
        threads=4,
        logger=None,
    )

    for fp in frames:
        if os.path.exists(fp):
            os.remove(fp)

    return output_path, {
        "title": theme["title"],
        "script": theme["script"],
        "duration": part_duration * 2,
        "hashtags": ["shorts", "kids", "funfacts", "learning", "education"],
    }


def generate_viral_shorts(output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(Config.OUTPUT_DIR, "shorts")
    os.makedirs(output_dir, exist_ok=True)

    results = []
    for i in range(1):
        output_path = os.path.join(output_dir, f"kids_short_{i+1}.mp4")
        try:
            path, info = create_kids_short(i, output_path)
            results.append({"path": path, "info": info})
            print(f"  Kids Short {i+1}: {info['title'][:50]}...")
        except Exception as e:
            print(f"  Kids Short {i+1} failed: {e}")

    return results


if __name__ == "__main__":
    results = generate_viral_shorts()
    for r in results:
        print(f"\nKids Short: {r['info']['title']}")
        print(f"  Duration: {r['info']['duration']}s")
        print(f"  Path: {r['path']}")
