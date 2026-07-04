import os
import random
import math
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from moviepy.audio.fx import AudioFadeIn, AudioFadeOut
from src.config import Config
from src.trends_fetcher import get_trending_kids_topics


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
        {"sky_top": (100, 180, 255), "sky_bot": (200, 230, 255), "ground": (50, 200, 100)},
        {"sky_top": (255, 150, 100), "sky_bot": (255, 200, 150), "ground": (150, 100, 200)},
        {"sky_top": (180, 100, 255), "sky_bot": (220, 180, 255), "ground": (50, 200, 150)},
        {"sky_top": (50, 200, 200), "sky_bot": (150, 230, 230), "ground": (100, 220, 100)},
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
    cloud_colors = [(255, 255, 255, 120), (255, 255, 255, 90), (240, 240, 255, 100)]
    for _ in range(5):
        cx = random.randint(100, W - 100)
        cy = random.randint(80, ground_y - 200)
        size = random.randint(50, 120)
        cc = random.choice(cloud_colors)
        draw.ellipse([cx - size, cy - size // 2, cx + size, cy + size // 2], fill=cc)
        draw.ellipse([cx - size // 2, cy - size // 3, cx + size // 2, cy + size // 3], fill=cc)
    star_colors = [(255, 215, 0, 180), (255, 255, 200, 150), (255, 200, 100, 160)]
    for _ in range(6):
        cx = random.randint(50, W - 50)
        cy = random.randint(50, ground_y - 300)
        size = random.randint(15, 30)
        _draw_star(draw, cx, cy, size, random.choice(star_colors))
    flower_colors = [(255, 100, 100), (255, 255, 100), (100, 255, 100), (255, 150, 200), (100, 200, 255)]
    for _ in range(8):
        cx = random.randint(100, W - 100)
        cy = random.randint(ground_y + 20, H - 50)
        rsize = random.randint(30, 70)
        draw.ellipse([cx - rsize, cy - rsize // 2, cx + rsize, cy + rsize // 2], fill=random.choice(flower_colors))
        draw.ellipse([cx - 5, cy - 8, cx + 5, cy + 5], fill=(255, 200, 50))
    return img


def _build_kids_facts():
    raw = get_trending_kids_topics()
    facts = []
    for topic in raw:
        facts.append({
            "title": f"Did You Know? {topic.title()}! #shorts #kids #funfacts",
            "script": f"Did you know? {topic}. Share this with a friend! Subscribe for more fun facts!",
        })
    return facts


def _create_kids_frame(W, H, bg_image):
    img = bg_image.copy()
    img = img.resize((W, H), Image.LANCZOS)
    draw = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2 + 50
    draw.ellipse([cx - 100, cy - 100, cx + 100, cy + 100], fill=(0, 0, 0, 120))
    draw.ellipse([cx - 95, cy - 95, cx + 95, cy + 95], outline=(255, 215, 0), width=4)
    play_x = cx - 35
    play_y = cy - 50
    draw.polygon([(play_x, play_y), (play_x, play_y + 100), (play_x + 80, play_y + 50)], fill=(255, 215, 0))
    draw.rectangle([0, 0, W, 6], fill=(255, 215, 0))
    draw.rectangle([0, H - 6, W, H], fill=(255, 215, 0))
    return img


def create_kids_short(fact_idx, facts, output_path, voice_path=None):
    W, H = 1080, 1920
    part_duration = 5
    bg_image = _create_cartoon_bg(fact_idx)
    frames = []
    for part in range(2):
        frame = _create_kids_frame(W, H, bg_image)
        frame_path = output_path.replace(".mp4", f"_part{part}.png")
        frame.save(frame_path, quality=95)
        frames.append(frame_path)
    clips = []
    for fp in frames:
        clip = ImageClip(fp, duration=part_duration)
        clip = clip.with_effects([AudioFadeIn(0.3), AudioFadeOut(0.3)])
        clips.append(clip)
    video = concatenate_videoclips(clips, method="compose")
    if voice_path and os.path.exists(voice_path) and os.path.getsize(voice_path) > 1000:
        audio = AudioFileClip(voice_path)
        video = video.with_audio(audio)
    video.write_videofile(output_path, fps=24, codec="libx264", preset="fast", threads=4, logger=None)
    for fp in frames:
        if os.path.exists(fp):
            os.remove(fp)
    theme = facts[fact_idx % len(facts)]
    return output_path, {
        "title": theme["title"],
        "script": theme["script"],
        "duration": part_duration * 2,
        "hashtags": ["shorts", "kids", "funfacts", "learning"],
    }


def generate_viral_shorts(output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(Config.OUTPUT_DIR, "shorts")
    os.makedirs(output_dir, exist_ok=True)
    facts = _build_kids_facts()
    results = []
    count = min(2, len(facts))
    for i in range(count):
        output_path = os.path.join(output_dir, f"kids_short_{i+1}.mp4")
        try:
            path, info = create_kids_short(i, facts, output_path)
            results.append({"path": path, "info": info})
            print(f"  Kids Short {i+1}: {info['title'][:50]}...")
        except Exception as e:
            print(f"  Kids Short {i+1} failed: {e}")
    return results


if __name__ == "__main__":
    results = generate_viral_shorts()
    for r in results:
        print(f"\nKids Short: {r['info']['title']}")
