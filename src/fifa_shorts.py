import os
import random
import urllib.request
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from moviepy.audio.fx import AudioFadeIn, AudioFadeOut
from src.config import Config
from src.trends_fetcher import get_trending_sports_topics


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


def _download_image(url, fallback_color=(255, 0, 0)):
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


def _get_short_images(theme_idx):
    image_queries = [
        [
            "https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=1080&h=1920&fit=crop",
            "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=1080&h=1920&fit=crop",
            "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=1080&h=1920&fit=crop",
            "https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=1080&h=1920&fit=crop",
        ],
        [
            "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=1080&h=1920&fit=crop",
            "https://images.unsplash.com/photo-1553778263-73a83bab9b0c?w=1080&h=1920&fit=crop",
            "https://images.unsplash.com/photo-1560272564-c83b66b1ad12?w=1080&h=1920&fit=crop",
            "https://images.unsplash.com/photo-1489944440615-453fc2b6a9a9?w=1080&h=1920&fit=crop",
        ],
    ]
    urls = image_queries[theme_idx % len(image_queries)]
    images = []
    for url in urls:
        img = _download_image(url)
        images.append(img)
    return images


def _build_viral_shorts():
    raw = get_trending_sports_topics()
    shorts = []
    for topic in raw:
        shorts.append({
            "title": f"{topic.title()} Will BLOW Your Mind! #shorts #football #viral",
            "script": f"Did you know? {topic}. Football history is full of amazing records. Subscribe for more!",
            "bg": [(random.randint(100, 255), random.randint(0, 100), 0)],
            "text": (255, 255, 255),
            "accent": (255, 215, 0),
            "hooks": ["STOP SCROLLING!", "THIS IS INSANE!", "NO WAY!", "WATCH THIS!"],
        })
    return shorts


def _create_viral_frame_with_image(W, H, theme, hook_text, bg_image, part=0):
    img = bg_image.copy()
    img = img.resize((W, H), Image.LANCZOS)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.4)
    img = img.filter(ImageFilter.GaussianBlur(radius=3))
    draw = ImageDraw.Draw(img)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    for i in range(3):
        y_start = 150 + i * 220
        ov_draw.rectangle([0, y_start, W, y_start + 180], fill=(0, 0, 0, 160))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    font_hook = _get_font(90)
    font_big = _get_font(72)
    font_med = _get_font(48)
    font_small = _get_font(36)
    hook_y = 200
    bbox = draw.textbbox((0, 0), hook_text, font=font_hook)
    tw = bbox[2] - bbox[0]
    draw.text((W // 2 - tw // 2 + 3, hook_y + 3), hook_text, fill=(0, 0, 0), font=font_hook)
    draw.text((W // 2 - tw // 2, hook_y), hook_text, fill=theme["accent"], font=font_hook)
    if part == 0:
        cx, cy = W // 2, H // 2 + 100
        draw.ellipse([cx - 120, cy - 120, cx + 120, cy + 120], fill=(0, 0, 0))
        draw.ellipse([cx - 115, cy - 115, cx + 115, cy + 115], outline=theme["accent"], width=4)
        draw.polygon([(cx - 40, cy - 60), (cx - 40, cy + 60), (cx + 60, cy)], fill=theme["accent"])
        draw.rectangle([60, H - 380, W - 60, H - 260], fill=(0, 0, 0))
        draw.rectangle([60, H - 380, W - 60, H - 260], outline=theme["accent"], width=4)
        bbox_sub = draw.textbbox((0, 0), "SUBSCRIBE NOW!", font=font_big)
        tw_sub = bbox_sub[2] - bbox_sub[0]
        draw.text((W // 2 - tw_sub // 2, H - 360), "SUBSCRIBE NOW!", fill=theme["accent"], font=font_big)
        stats = [("3B+", "FANS"), ("200+", "COUNTRIES"), ("1M+", "GOALS")]
        for i, (num, label) in enumerate(stats):
            x = 180 + i * 270
            y = H // 2 + 300
            draw.rectangle([x - 80, y - 40, x + 80, y + 40], fill=(0, 0, 0))
            draw.rectangle([x - 80, y - 40, x + 80, y + 40], outline=theme["accent"], width=2)
            bbox_n = draw.textbbox((0, 0), num, font=font_med)
            tw_n = bbox_n[2] - bbox_n[0]
            draw.text((x - tw_n // 2, y - 30), num, fill=theme["accent"], font=font_med)
            bbox_l = draw.textbbox((0, 0), label, font=font_small)
            tw_l = bbox_l[2] - bbox_l[0]
            draw.text((x - tw_l // 2, y + 10), label, fill=(255, 255, 255), font=font_small)
    elif part == 1:
        numbers = ["3B", "200", "40K", "1000"]
        labels = ["FANS", "COUNTRIES", "STADIUMS", "LEGENDS"]
        for i, (num, label) in enumerate(zip(numbers, labels)):
            x = 135 + i * 270
            y_center = H // 2
            draw.ellipse([x - 70, y_center - 70, x + 70, y_center + 70], fill=(0, 0, 0))
            draw.ellipse([x - 65, y_center - 65, x + 65, y_center + 65], outline=theme["accent"], width=3)
            bbox_n = draw.textbbox((0, 0), num, font=font_big)
            tw_n = bbox_n[2] - bbox_n[0]
            draw.text((x - tw_n // 2, y_center - 35), num, fill=theme["accent"], font=font_big)
            bbox_l = draw.textbbox((0, 0), label, font=font_med)
            tw_l = bbox_l[2] - bbox_l[0]
            draw.text((x - tw_l // 2, y_center + 45), label, fill=theme["text"], font=font_med)
        draw.rectangle([60, H - 300, W - 60, H - 200], fill=(255, 0, 0))
        bbox_like = draw.textbbox((0, 0), "LIKE & SHARE!", font=font_big)
        tw_like = bbox_like[2] - bbox_like[0]
        draw.text((W // 2 - tw_like // 2, H - 285), "LIKE & SHARE!", fill=(255, 255, 255), font=font_big)
    draw.rectangle([0, 0, W, 6], fill=theme["accent"])
    draw.rectangle([0, H - 6, W, H], fill=theme["accent"])
    return img


def create_viral_short(theme_idx, themes, output_path, voice_path=None):
    theme = themes[theme_idx % len(themes)]
    W, H = 1080, 1920
    part_duration = 4
    bg_images = _get_short_images(theme_idx)
    frames = []
    for part in range(2):
        hook = theme["hooks"][part % len(theme["hooks"])]
        bg_img = bg_images[part % len(bg_images)]
        frame = _create_viral_frame_with_image(W, H, theme, hook, bg_img, part)
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
    return output_path, {
        "title": theme["title"],
        "script": theme["script"],
        "duration": part_duration * 2,
        "hashtags": ["shorts", "football", "viral", "soccer", "sports"],
    }


def generate_viral_shorts(output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(Config.OUTPUT_DIR, "shorts")
    os.makedirs(output_dir, exist_ok=True)
    themes = _build_viral_shorts()
    results = []
    count = min(2, len(themes))
    for i in range(count):
        output_path = os.path.join(output_dir, f"viral_short_{i+1}.mp4")
        try:
            path, info = create_viral_short(i, themes, output_path)
            results.append({"path": path, "info": info})
            print(f"  Viral Short {i+1}: {info['title'][:50]}...")
        except Exception as e:
            print(f"  Viral Short {i+1} failed: {e}")
    return results


if __name__ == "__main__":
    results = generate_viral_shorts()
    for r in results:
        print(f"\nViral Short: {r['info']['title']}")
        print(f"  Duration: {r['info']['duration']}s")
        print(f"  Path: {r['info']['path']}")
