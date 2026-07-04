import os
import random
import math
import urllib.request
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from moviepy import (
    ImageClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip,
    concatenate_videoclips, TextClip, ColorClip
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


def _download_picsum(path, seed):
    try:
        url = f"https://picsum.photos/seed/{seed}/1080/1920"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=15).read()
        if len(data) > 5000:
            with open(path, "wb") as f:
                f.write(data)
            return True
    except Exception:
        pass
    return False


def _get_short_bg_image(seed_base):
    seeds = [f"{seed_base}_{i}" for i in range(1, 5)]
    for seed in seeds:
        path = os.path.join(Config.OUTPUT_DIR, f"short_bg_{seed}.jpg")
        ok = _download_picsum(path, seed)
        if ok:
            img = Image.open(path).convert("RGB")
            return img
    return None


SHORT_THEMES = [
    {
        "title": "This GOAL Broke The Internet! #shorts #football",
        "script": "This goal from the World Cup qualifiers absolutely broke the internet. The technique, the power, the placement. Pure perfection. Would you score from this angle?",
        "accent": (255, 0, 0),
        "text_color": (255, 215, 0),
        "seed": "football_goal_amazing",
    },
    {
        "title": "World Cup 2026 SECRET Revealed! #shorts #worldcup",
        "script": "Here is a World Cup 2026 secret that nobody is talking about. 48 teams, 104 matches, 39 days. The biggest World Cup ever. Are you ready?",
        "accent": (255, 215, 0),
        "text_color": (255, 255, 255),
        "seed": "worldcup_secret_2026",
    },
    {
        "title": "The SAVE That Won The Match! #shorts #soccer",
        "script": "This goalkeeper save is absolutely insane. Diving full stretch to keep the ball out. This is what separates the best from the rest.",
        "accent": (255, 255, 0),
        "text_color": (255, 255, 255),
        "seed": "goalkeeper_save_epic",
    },
    {
        "title": "Football Fans Go CRAZY! #shorts #fans",
        "script": "Listen to these football fans. The passion, the energy, the atmosphere. This is why we love the beautiful game.",
        "accent": (0, 255, 0),
        "text_color": (255, 255, 255),
        "seed": "football_fans_crazy",
    },
    {
        "title": "Skill Move That FOOLED Everyone! #shorts #skills",
        "script": "This skill move completely fooled the defender. The fake, the turn, the acceleration. Pure magic on the football pitch.",
        "accent": (0, 200, 255),
        "text_color": (255, 255, 255),
        "seed": "football_skill_magic",
    },
    {
        "title": "World Cup Stadiums Are INSANE! #shorts #stadium",
        "script": "Take a look at these World Cup 2026 stadiums. MetLife, AT&T, SoFi. 82,000 fans screaming. Incredible.",
        "accent": (255, 215, 0),
        "text_color": (255, 255, 255),
        "seed": "stadium_worldcup_2026",
    },
    {
        "title": "HAT-TRICK Hero! #shorts #football",
        "script": "Three goals, one player, absolute domination. This hat-trick performance is one of the best we have ever seen.",
        "accent": (255, 215, 0),
        "text_color": (255, 255, 255),
        "seed": "hattrick_football_hero",
    },
    {
        "title": "Red Card CHAOS! #shorts #drama",
        "script": "This red card caused absolute chaos. The referee, the protests, the drama. Football is nothing without moments like this.",
        "accent": (255, 255, 255),
        "text_color": (255, 215, 0),
        "seed": "red_card_chaos",
    },
]


def _create_short_bg_with_image(W, H, theme, bg_image):
    img = bg_image.copy()
    img = img.resize((W, H), Image.LANCZOS)

    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.35)

    img = img.filter(ImageFilter.GaussianBlur(radius=4))

    draw = ImageDraw.Draw(img)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)

    ov_draw.rectangle([0, 250, W, 750], fill=(0, 0, 0, 180))
    ov_draw.rectangle([0, H - 350, W, H - 180], fill=(0, 0, 0, 180))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 6], fill=theme["accent"])
    draw.rectangle([0, H - 6, W, H], fill=theme["accent"])

    return img


def create_short_video(theme_idx, output_path, voice_path=None):
    theme = SHORT_THEMES[theme_idx % len(SHORT_THEMES)]
    W, H = 1080, 1920

    bg_img = _get_short_bg_image(theme["seed"])
    if bg_img is None:
        bg_img = Image.new("RGB", (W, H), (20, 40, 80))

    bg = _create_short_bg_with_image(W, H, theme, bg_img)
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

    cx, cy = W // 2, H // 2 + 50
    draw.ellipse([cx - 100, cy - 100, cx + 100, cy + 100], fill=(0, 0, 0))
    draw.ellipse([cx - 95, cy - 95, cx + 95, cy + 95], outline=theme["accent"], width=4)
    draw.polygon([(cx - 35, cy - 50), (cx - 35, cy + 50), (cx + 50, cy)], fill=theme["accent"])

    draw.rectangle([60, H - 300, W - 60, H - 200], fill=(255, 0, 0))
    bbox_sub = draw.textbbox((0, 0), "SUBSCRIBE!", font=font_huge)
    tw_sub = bbox_sub[2] - bbox_sub[0]
    draw.text((W // 2 - tw_sub // 2, H - 290), "SUBSCRIBE!", fill=(255, 255, 255), font=font_huge)

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

    bg_clip = bg_clip.with_effects([AudioFadeIn(0.5), AudioFadeOut(0.5)])

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


def generate_shorts_batch(count=1, output_dir=None):
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
    results = generate_shorts_batch(1)
    for r in results:
        print(f"\nShort: {r['info']['title']}")
        print(f"  Duration: {r['info']['duration']}s")
        print(f"  Path: {r['path']}")
