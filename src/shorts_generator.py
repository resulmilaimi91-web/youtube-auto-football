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


def _download_image(url, fallback_color=(20, 40, 80)):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=10).read()
        return Image.open(io.BytesIO(data)).convert("RGB")
    except Exception:
        img = Image.new("RGB", (1080, 1920), fallback_color)
        draw = ImageDraw.Draw(img)
        for y in range(1920):
            ratio = y / 1920
            r = int(fallback_color[0] * (1 - ratio * 0.3))
            g = int(fallback_color[1] * (1 - ratio * 0.3))
            b = int(fallback_color[2] * (1 - ratio * 0.3))
            draw.line([(0, y), (1080, y)], fill=(r, g, b))
        return img


SHORT_THEMES = [
    {
        "title": "This GOAL Broke The Internet! #shorts #football",
        "script": "This goal from the World Cup qualifiers absolutely broke the internet. The technique, the power, the placement. Pure perfection. Would you score from this angle?",
        "images": [
            "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=1080&h=1920&fit=crop",
            "https://images.unsplash.com/photo-1553778263-73a83bab9b0c?w=1080&h=1920&fit=crop",
        ],
        "accent": (255, 0, 0),
        "text_color": (255, 215, 0),
    },
    {
        "title": "World Cup 2026 SECRET Revealed! #shorts #worldcup",
        "script": "Here is a World Cup 2026 secret that nobody is talking about. 48 teams, 104 matches, 39 days. The biggest World Cup ever. Are you ready?",
        "images": [
            "https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=1080&h=1920&fit=crop",
            "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=1080&h=1920&fit=crop",
        ],
        "accent": (255, 215, 0),
        "text_color": (255, 255, 255),
    },
    {
        "title": "The SAVE That Won The Match! #shorts #soccer",
        "script": "This goalkeeper save is absolutely insane. Diving full stretch to keep the ball out. This is what separates the best from the rest.",
        "images": [
            "https://images.unsplash.com/photo-1560272564-c83b66b1ad12?w=1080&h=1920&fit=crop",
            "https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=1080&h=1920&fit=crop",
        ],
        "accent": (255, 255, 0),
        "text_color": (255, 255, 255),
    },
    {
        "title": "Football Fans Go CRAZY! #shorts #fans",
        "script": "Listen to these football fans. The passion, the energy, the atmosphere. This is why we love the beautiful game.",
        "images": [
            "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=1080&h=1920&fit=crop",
            "https://images.unsplash.com/photo-1489944440615-453fc2b6a9a9?w=1080&h=1920&fit=crop",
        ],
        "accent": (0, 255, 0),
        "text_color": (255, 255, 255),
    },
    {
        "title": "Skill Move That FOOLED Everyone! #shorts #skills",
        "script": "This skill move completely fooled the defender. The fake, the turn, the acceleration. Pure magic on the football pitch.",
        "images": [
            "https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=1080&h=1920&fit=crop",
            "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=1080&h=1920&fit=crop",
        ],
        "accent": (0, 200, 255),
        "text_color": (255, 255, 255),
    },
    {
        "title": "World Cup Stadiums Are INSANE! #shorts #stadium",
        "script": "Take a look at these World Cup 2026 stadiums. MetLife, Azteca, SoFi. 82,000 fans screaming. Incredible.",
        "images": [
            "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=1080&h=1920&fit=crop",
            "https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=1080&h=1920&fit=crop",
        ],
        "accent": (255, 215, 0),
        "text_color": (255, 255, 255),
    },
    {
        "title": "HAT-TRICK Hero! #shorts #football",
        "script": "Three goals, one player, absolute domination. This hat-trick performance is one of the best we have ever seen.",
        "images": [
            "https://images.unsplash.com/photo-1553778263-73a83bab9b0c?w=1080&h=1920&fit=crop",
            "https://images.unsplash.com/photo-1560272564-c83b66b1ad12?w=1080&h=1920&fit=crop",
        ],
        "accent": (255, 215, 0),
        "text_color": (255, 255, 255),
    },
    {
        "title": "Red Card CHAOS! #shorts #drama",
        "script": "This red card caused absolute chaos. The referee, the protests, the drama. Football is nothing without moments like this.",
        "images": [
            "https://images.unsplash.com/photo-1489944440615-453fc2b6a9a9?w=1080&h=1920&fit=crop",
            "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=1080&h=1920&fit=crop",
        ],
        "accent": (255, 255, 255),
        "text_color": (255, 215, 0),
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

    img_urls = theme.get("images", [])
    bg_image = None
    for url in img_urls:
        bg_image = _download_image(url)
        if bg_image:
            break

    if bg_image is None:
        bg_image = Image.new("RGB", (W, H), (20, 40, 80))

    bg = _create_short_bg_with_image(W, H, theme, bg_image)
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
