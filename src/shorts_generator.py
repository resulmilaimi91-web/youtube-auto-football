import os
import random
import math
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    ImageClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip,
    concatenate_videoclips, afx, TextClip, ColorClip
)
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


SHORT_THEMES = [
    {
        "title": "This GOAL Broke The Internet! #shorts #football",
        "script": "This goal from the World Cup qualifiers absolutely broke the internet. The technique, the power, the placement. Pure perfection. Would you score from this angle?",
        "bg_colors": [(10, 20, 60), (0, 50, 120)],
        "accent": (255, 0, 0),
        "text_color": (255, 215, 0),
    },
    {
        "title": "World Cup 2026 SECRET Revealed! #shorts #worldcup",
        "script": "Here is a World Cup 2026 secret that nobody is talking about. 48 teams, 104 matches, 39 days. The biggest World Cup ever. Are you ready?",
        "bg_colors": [(0, 30, 80), (0, 80, 160)],
        "accent": (255, 215, 0),
        "text_color": (255, 255, 255),
    },
    {
        "title": "The SAVE That Won The Match! #shorts #soccer",
        "script": "This goalkeeper save is absolutely insane. Diving full stretch to keep the ball out. This is what separates the best from the rest.",
        "bg_colors": [(20, 40, 20), (0, 100, 0)],
        "accent": (255, 255, 0),
        "text_color": (255, 255, 255),
    },
    {
        "title": "Football Fans Go CRAZY! #shorts #fans",
        "script": "Listen to these football fans. The passion, the energy, the atmosphere. This is why we love the beautiful game.",
        "bg_colors": [(60, 10, 60), (120, 20, 80)],
        "accent": (0, 255, 0),
        "text_color": (255, 255, 255),
    },
    {
        "title": "Skill Move That FOOLED Everyone! #shorts #skills",
        "script": "This skill move completely fooled the defender. The fake, the turn, the acceleration. Pure magic on the football pitch.",
        "bg_colors": [(40, 20, 0), (100, 50, 0)],
        "accent": (0, 200, 255),
        "text_color": (255, 255, 255),
    },
    {
        "title": "World Cup Stadiums Are INSANE! #shorts #stadium",
        "script": "Take a look at these World Cup 2026 stadiums. MetLife, Azteca, SoFi. 82,000 fans screaming. Incredible.",
        "bg_colors": [(10, 10, 40), (30, 30, 80)],
        "accent": (255, 215, 0),
        "text_color": (255, 255, 255),
    },
    {
        "title": "HAT-TRICK Hero! #shorts #football",
        "script": "Three goals, one player, absolute domination. This hat-trick performance is one of the best we have ever seen.",
        "bg_colors": [(60, 0, 0), (120, 20, 20)],
        "accent": (255, 215, 0),
        "text_color": (255, 255, 255),
    },
    {
        "title": "Red Card CHAOS! #shorts #drama",
        "script": "This red card caused absolute chaos. The referee, the protests, the drama. Football is nothing without moments like this.",
        "bg_colors": [(40, 0, 0), (80, 0, 0)],
        "accent": (255, 255, 255),
        "text_color": (255, 215, 0),
    },
]


def _create_short_bg(W, H, colors, accent):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    c1, c2 = colors

    for y in range(H):
        ratio = y / H
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    for i in range(40):
        x = random.randint(0, W)
        y = random.randint(0, H)
        size = random.randint(2, 6)
        draw.ellipse([x - size, y - size, x + size, y + size], fill=(255, 255, 255))

    draw.rectangle([0, 0, W, 6], fill=accent)
    draw.rectangle([0, H - 6, W, H], fill=accent)

    return img


def create_short_video(theme_idx, output_path, voice_path=None):
    theme = SHORT_THEMES[theme_idx % len(SHORT_THEMES)]
    W, H = 1080, 1920

    bg = _create_short_bg(W, H, theme["bg_colors"], theme["accent"])
    draw = ImageDraw.Draw(bg)

    font_huge = _get_font(80)
    font_big = _get_font(56)
    font_med = _get_font(40)
    font_small = _get_font(32)

    title_words = theme["title"].split("#")[0].strip().split()
    y_pos = 300
    for word in title_words[:5]:
        bbox = draw.textbbox((0, 0), word, font=font_huge)
        tw = bbox[2] - bbox[0]
        draw.text((W // 2 - tw // 2 + 4, y_pos + 4), word, fill=(0, 0, 0), font=font_huge)
        draw.text((W // 2 - tw // 2, y_pos), word, fill=theme["text_color"], font=font_huge)
        y_pos += 95

    cx, cy = W // 2, H // 2
    draw.ellipse([cx - 120, cy - 120, cx + 120, cy + 120], fill=(255, 255, 255))
    draw.polygon([(cx - 40, cy - 60), (cx - 40, cy + 60), (cx + 60, cy)], fill=theme["accent"])

    draw.rectangle([60, H - 300, W - 60, H - 200], fill=(255, 0, 0))
    draw.text((W // 2 - 180, H - 290), "SUBSCRIBE!", fill=(255, 255, 255), font=font_huge)

    bg_path = output_path.replace(".mp4", "_bg.png")
    bg.save(bg_path, quality=95)

    bg_clip = ImageClip(bg_path, duration=10)

    if voice_path and os.path.exists(voice_path) and os.path.getsize(voice_path) > 1000:
        audio = AudioFileClip(voice_path)
        duration = audio.duration + 1
        bg_clip = bg_clip.with_duration(duration)
        final_audio = audio
    else:
        duration = 10
        bg_clip = bg_clip.with_duration(duration)
        final_audio = None

    bg_clip = bg_clip.with_effects([afx.FadeIn(0.5), afx.FadeOut(0.5)])

    if final_audio:
        bg_clip = bg_clip.with_audio(final_audio)

    bg_clip.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac" if final_audio else None,
        preset="fast",
        threads=4,
        logger=None,
    )

    if os.path.exists(bg_path):
        os.remove(bg_path)

    return output_path, {
        "title": theme["title"],
        "script": theme["script"],
        "duration": duration,
        "hashtags": ["shorts", "football", "worldcup2026", "soccer", "fifa"],
    }


def generate_shorts_batch(count=6, output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(Config.OUTPUT_DIR, "shorts")
    os.makedirs(output_dir, exist_ok=True)

    results = []
    for i in range(count):
        output_path = os.path.join(output_dir, f"short_{i+1}.mp4")
        theme_idx = i % len(SHORT_THEMES)
        try:
            path, info = create_short_video(theme_idx, output_path)
            results.append({"path": path, "info": info})
            print(f"  Short {i+1}: {info['title'][:50]}...")
        except Exception as e:
            print(f"  Short {i+1} failed: {e}")

    return results


if __name__ == "__main__":
    results = generate_shorts_batch(3)
    for r in results:
        print(f"\nShort: {r['info']['title']}")
        print(f"  Duration: {r['info']['duration']}s")
        print(f"  Path: {r['path']}")
