import os
import random
import urllib.request
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx import FadeIn, FadeOut


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


def _get_theme_images(theme, count=10):
    queries = {
        "rainbow": ["rainbow+nature", "colorful+sky", "rainbow+clouds", "flowers+rainbow", "sun+rainbow"],
        "bunny": ["cute+bunny", "rabbit+nature", "baby+rabbit", "bunny+grass", "fluffy+rabbit"],
        "stars": ["night+sky+stars", "stars+galaxy", "starry+night", "twinkling+stars", "moon+stars"],
        "fish": ["colorful+fish", "underwater+ocean", "tropical+fish", "sea+life", "aquarium+fish"],
        "train": ["colorful+train", "train+railway", "kids+train", "toy+train", "train+nature"],
        "cat": ["cute+cat+kitten", "fluffy+cat", "kitten+playful", "cat+nature", "sleeping+cat"],
        "morning": ["sunrise+nature", "morning+sunshine", "sunrise+landscape", "morning+flowers", "sunrise+sky"],
    }
    keywords = queries.get(theme, ["nature+landscape", "colorful+nature", "beautiful+scenery"])

    paths = []
    os.makedirs("output", exist_ok=True)
    for i in range(count):
        kw = random.choice(keywords)
        path = f"output/kids_img_{theme}_{i}.jpg"
        try:
            url = f"https://picsum.photos/seed/kids{theme}{i}/1920/1080"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=10).read()
            if len(data) > 5000:
                with open(path, "wb") as f:
                    f.write(data)
                if os.path.getsize(path) > 10000:
                    paths.append(path)
                    continue
        except Exception:
            pass
        img = Image.new("RGB", (1920, 1080), (40, 40, 80))
        draw = ImageDraw.Draw(img)
        for y in range(1080):
            r = int(30 + 20 * (y / 1080))
            g = int(40 + 30 * (y / 1080))
            b = int(70 + 20 * (y / 1080))
            draw.line([(0, y), (1920, y)], fill=(r, g, b))
        font = _get_font(80)
        lines = kw.replace("+", " ").title().split()
        display = " ".join(lines[:3])
        bbox = draw.textbbox((0, 0), display, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((1920 - tw) // 2, 480), display, fill=(255, 255, 255), font=font)
        draw.text(((1920 - tw) // 2 + 3, 483), display, fill=(100, 100, 200), font=font)
        img.save(path, quality=92)
        paths.append(path)
    return paths


def _add_text_overlay(img_path, lyrics_group, line_index, total_groups, W=1920, H=1080):
    img = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([0, H - 200, W, H], fill=(0, 0, 0, 160))
    overlay_draw.rectangle([0, 0, W, 80], fill=(0, 0, 0, 120))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    font_large = _get_font(52)
    font_small = _get_font(28)

    y_pos = H - 170
    for line in lyrics_group:
        if not line.strip():
            y_pos += 30
            continue
        bbox = draw.textbbox((0, 0), line, font=font_large)
        tw = bbox[2] - bbox[0]
        x_pos = (W - tw) // 2
        draw.text((x_pos + 2, y_pos + 2), line, fill=(0, 0, 0), font=font_large)
        draw.text((x_pos, y_pos), line, fill=(255, 255, 255), font=font_large)
        y_pos += 55

    progress = f"  {line_index + 1}/{total_groups}"
    draw.text((W - 120, 20), progress, fill=(200, 200, 200), font=font_small)

    subscribe = "♥ SUBSCRIBE"
    draw.text((20, 20), subscribe, fill=(255, 200, 50), font=font_small)

    channel = "KIDS SONGS"
    bbox = draw.textbbox((0, 0), channel, font=font_small)
    draw.text((W - bbox[2] - 20, 45), channel, fill=(255, 255, 255), font=font_small)

    return img


def create_kids_song_video(song_data, output_path, voice_path=None, W=1920, H=1080):
    lyrics = song_data["lyrics"]
    theme = song_data.get("theme", "rainbow")
    total_duration = 60
    if voice_path and os.path.exists(voice_path) and os.path.getsize(voice_path) > 1000:
        try:
            audio = AudioFileClip(voice_path)
            total_duration = max(audio.duration + 2, 30)
        except Exception:
            total_duration = 60

    line_groups = []
    group_size = max(1, len(lyrics) // max(1, int(total_duration // 7)))
    for i in range(0, len(lyrics), group_size):
        group = lyrics[i:i + group_size]
        if any(l.strip() for l in group):
            line_groups.append(group)

    num_images = max(len(line_groups), 5)
    img_paths = _get_theme_images(theme, num_images)

    clips = []
    for gi, group in enumerate(line_groups):
        if gi < len(img_paths):
            scene_img = _add_text_overlay(img_paths[gi], group, gi, len(line_groups), W, H)
        else:
            scene_img = _add_text_overlay(img_paths[-1], group, gi, len(line_groups), W, H)

        scene_path = output_path.replace(".mp4", f"_scene{gi}.png")
        scene_img.save(scene_path, quality=92)

        seg_dur = total_duration / len(line_groups)
        clip = ImageClip(scene_path, duration=seg_dur)
        clip = clip.with_effects([FadeIn(0.3), FadeOut(0.3)])
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")

    if voice_path and os.path.exists(voice_path) and os.path.getsize(voice_path) > 1000:
        try:
            audio = AudioFileClip(voice_path)
            video = video.with_audio(audio)
        except Exception:
            pass

    video.write_videofile(output_path, fps=24, codec="libx264", preset="fast", threads=4, logger=None)

    for gi in range(len(line_groups)):
        p = output_path.replace(".mp4", f"_scene{gi}.png")
        if os.path.exists(p):
            os.remove(p)
    for p in img_paths:
        if os.path.exists(p):
            os.remove(p)

    thumb_path = output_path.replace(".mp4", "_thumb.jpg")
    if img_paths and os.path.exists(img_paths[0]):
        thumb = Image.open(img_paths[0]).convert("RGB").resize((1280, 720))
    else:
        thumb = Image.new("RGB", (1280, 720), (40, 40, 80))
    draw = ImageDraw.Draw(thumb)
    title = song_data.get("title", "Kids Song")
    font_large = _get_font(56)
    bbox = draw.textbbox((0, 0), title, font=font_large)
    tw = bbox[2] - bbox[0]
    draw.rectangle([(1280 - tw) // 2 - 20, 300, (1280 + tw) // 2 + 20, 380], fill=(0, 0, 0, 180))
    draw.text(((1280 - tw) // 2, 310), title, fill=(255, 255, 255), font=font_large)
    thumb.save(thumb_path, quality=90)

    return output_path, thumb_path
