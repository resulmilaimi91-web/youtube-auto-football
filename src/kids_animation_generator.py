import os
import math
import random
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx import FadeIn, FadeOut
from moviepy.audio.fx import AudioFadeIn, AudioFadeOut


def _get_font(size):
    fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for path in fonts:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _draw_bunny(draw, cx, cy, size, color):
    body_color = (255, 220, 200) if color == "white" else (180, 160, 140)
    ear_color = (255, 200, 200)
    draw.ellipse([cx - size, cy - size // 2, cx + size, cy + size // 2], fill=body_color)
    draw.ellipse([cx - size // 3, cy - size, cx + size // 3, cy], fill=ear_color)
    draw.ellipse([cx - size // 5, cy - size * 1.2, cx + size // 5, cy - size // 4], fill=(255, 220, 220))
    draw.ellipse([cx - size // 4, cy - size // 4, cx, cy + size // 6], fill=(0, 0, 0))
    draw.ellipse([cx, cy - size // 4, cx + size // 4, cy + size // 6], fill=(0, 0, 0))
    draw.ellipse([cx - size // 8, cy - size // 2, cx + size // 8, cy - size // 3], fill=(255, 150, 150))
    draw.ellipse([cx - size // 10, cy - size // 2.5, cx + size // 10, cy - size // 3.5], fill=(255, 100, 100))


def _draw_fish(draw, cx, cy, size, color):
    fish_color = (255, 200, 50) if color == "gold" else (100, 200, 255)
    draw.ellipse([cx - size, cy - size // 2, cx + size, cy + size // 2], fill=fish_color)
    draw.polygon([(cx + size, cy), (cx + size + size // 2, cy - size // 2), (cx + size + size // 2, cy + size // 2)], fill=fish_color)
    draw.ellipse([cx - size // 4, cy - size // 6, cx, cy + size // 6], fill=(0, 0, 0))
    bubble_colors = [(255, 255, 255, 180), (200, 230, 255, 180), (255, 200, 200, 180)]
    for i in range(3):
        bx = cx - size + random.randint(-size // 4, size // 2)
        by = cy - size // 2 - random.randint(0, size // 3)
        bs = random.randint(4, 10)
        draw.ellipse([bx - bs, by - bs, bx + bs, by + bs], fill=random.choice(bubble_colors))


def _draw_star(draw, cx, cy, size, color):
    points = []
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        r = size if i % 2 == 0 else size // 2
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))
    draw.polygon(points, fill=(255, 215, 0))
    draw.ellipse([cx - size // 3, cy - size // 3, cx + size // 3, cy + size // 3], fill=(255, 255, 200))


def _draw_rainbow(draw, W, H, offset_y=0):
    rainbow_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (128, 0, 128)]
    for i, color in enumerate(rainbow_colors):
        y_offset = offset_y + i * 20
        for x in range(W):
            for y in range(H):
                dx = x - W // 2
                dy = y - (H // 2 - 100 + y_offset)
                dist = math.sqrt(dx * dx + dy * dy)
                if 180 - i * 15 <= dist <= 200 - i * 15:
                    draw.point((x, y), fill=color)


def _draw_train(draw, cx, cy, size):
    draw.rectangle([cx - size, cy - size // 2, cx + size, cy + size // 2], fill=(255, 50, 50))
    draw.rectangle([cx + size // 4, cy - size // 3, cx + size - size // 4, cy - size // 6], fill=(255, 200, 0))
    draw.ellipse([cx - size // 2, cy + size // 3, cx - size // 4, cy + size // 2], fill=(50, 50, 50))
    draw.ellipse([cx + size // 4, cy + size // 3, cx + size // 2, cy + size // 2], fill=(50, 50, 50))
    draw.rectangle([cx + size, cy - size // 3, cx + size + size // 3, cy + size // 3], fill=(255, 100, 0))
    draw.ellipse([cx + size + size // 6, cy + size // 6, cx + size + size // 3, cy + size // 3], fill=(50, 50, 50))
    for i in range(3):
        sx = cx + size // 4 + i * (size // 4)
        draw.rectangle([sx - 2, cy - size // 2 - size // 4, sx + 2, cy - size // 2], fill=(200, 200, 200))


def _draw_clouds(draw, W, H):
    for i in range(3):
        cx = random.randint(100, W - 100)
        cy = random.randint(30, H // 3)
        cloud_color = (255, 255, 255)
        for r in range(3):
            rx = cx + r * 30 - 30
            ry = cy + (r % 2) * 15
            rs = random.randint(30, 50)
            draw.ellipse([rx - rs, ry - rs, rx + rs, ry + rs], fill=cloud_color)


def _draw_balloons(draw, W, H, count=4):
    balloon_colors = [(255, 50, 50), (50, 200, 50), (50, 50, 255), (255, 200, 50), (255, 50, 200), (200, 50, 255)]
    for i in range(count):
        cx = random.randint(80, W - 80)
        cy = random.randint(80, H - 200)
        size = random.randint(25, 45)
        color = random.choice(balloon_colors)
        draw.ellipse([cx - size, cy - size, cx + size, cy + size], fill=color)
        draw.line([(cx, cy + size), (cx, cy + size + 30)], fill=(150, 150, 150), width=2)
        draw.polygon([(cx - 3, cy + size), (cx + 3, cy + size), (cx, cy + size + 8)], fill=(150, 150, 150))
        draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 200))


def _draw_sun(draw, W, H):
    sun_x = W - 80
    sun_y = 80
    for r in range(60, 0, -5):
        alpha = int(255 * (1 - r / 60))
        draw.ellipse([sun_x - r, sun_y - r, sun_x + r, sun_y + r], fill=(255, 220, 50, alpha))
    draw.ellipse([sun_x - 40, sun_y - 40, sun_x + 40, sun_y + 40], fill=(255, 200, 0))
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        dx = int(55 * math.cos(rad))
        dy = int(55 * math.sin(rad))
        draw.line([(sun_x + dx, sun_y + dy), (sun_x + dx * 2, sun_y + dy * 2)], fill=(255, 200, 0), width=3)


def _draw_grass(draw, W, H):
    grass_colors = [(50, 180, 50), (40, 160, 40), (60, 200, 60)]
    for x in range(0, W, 5):
        y = H - random.randint(0, 20)
        color = random.choice(grass_colors)
        for _ in range(3):
            h = random.randint(10, 30)
            draw.line([(x, y), (x + random.randint(-5, 5), y - h)], fill=color, width=2)


def _draw_flowers(draw, W, H):
    flower_colors = [(255, 100, 100), (255, 200, 100), (255, 100, 200), (200, 100, 255), (100, 200, 255)]
    for i in range(6):
        fx = random.randint(30, W - 30)
        fy = H - random.randint(10, 40)
        draw.line([(fx, fy), (fx, fy - random.randint(20, 40))], fill=(50, 180, 50), width=3)
        fc = random.choice(flower_colors)
        for p in range(5):
            angle = math.radians(p * 72)
            px = fx + int(10 * math.cos(angle))
            py = fy - 30 + int(10 * math.sin(angle))
            draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=fc)
        draw.ellipse([fx - 4, fy - 34, fx + 4, fy - 26], fill=(255, 255, 50))


def create_scene(theme, line_count, W=1080, H=1920):
    img = Image.new("RGB", (W, H))

    bg_colors = {
        "rainbow": (135, 206, 235),
        "bunny": (180, 230, 180),
        "stars": (20, 20, 80),
        "fish": (100, 200, 230),
        "train": (200, 230, 255),
        "cat": (255, 220, 200),
        "morning": (255, 240, 200),
    }
    bg = bg_colors.get(theme, (200, 220, 255))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        r = int(bg[0] + (bg[0] // 2) * ratio)
        g = int(bg[1] + (bg[1] // 2) * ratio)
        b = int(bg[2] + (bg[2] // 2) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    if theme == "rainbow":
        _draw_rainbow(draw, W, H, offset_y=200)
        _draw_clouds(draw, W, H)
        _draw_sun(draw, W, H)
    elif theme == "bunny":
        _draw_grass(draw, W, H)
        _draw_flowers(draw, W, H)
        _draw_clouds(draw, W, H)
        _draw_sun(draw, W, H)
        _draw_bunny(draw, W // 2, H // 2 + 100, 80, "white")
        for i in range(2):
            bx = W // 4 + i * (W // 2)
            by = H // 3 + random.randint(50, 150)
            _draw_balloons(draw, W, H, 3)
    elif theme == "stars":
        for i in range(80):
            sx = random.randint(0, W)
            sy = random.randint(0, H)
            ss = random.randint(1, 3)
            draw.ellipse([sx - ss, sy - ss, sx + ss, sy + ss], fill=(255, 255, 255))
        _draw_star(draw, W // 2, H // 2 - 100, 60, "gold")
        _draw_star(draw, W // 3, H // 3, 40, "gold")
        _draw_star(draw, 2 * W // 3, H // 3 + 50, 45, "gold")
        _draw_star(draw, W // 2, 2 * H // 3, 50, "gold")
        moon_color = (240, 240, 255)
        draw.ellipse([W - 120, 40, W - 20, 140], fill=moon_color)
        draw.ellipse([W - 100, 30, W, 130], fill=(20, 20, 80))
    elif theme == "fish":
        for y in range(H // 2, H):
            ratio = (y - H // 2) / (H // 2)
            r = int(30 + 50 * ratio)
            g = int(80 + 100 * ratio)
            b = int(150 + 50 * ratio)
            draw.line([(0, y), (W, y)], fill=(r, g, b))
        for i in range(3):
            y_offset = 40 * i
            draw.ellipse([W // 4, H // 2 + 50 + y_offset, 3 * W // 4, H // 2 + 80 + y_offset], fill=(200, 230, 255, 100))
        _draw_fish(draw, W // 2, H // 2 + 120, 60, "gold")
        _draw_fish(draw, W // 3, H // 2 + 50, 40, "blue")
        _draw_fish(draw, 2 * W // 3, H // 2 + 80, 35, "blue")
        for i in range(4):
            bx = random.randint(50, W - 50)
            by = H // 2 + 50 + random.randint(0, H // 3)
            draw.ellipse([bx - 15, by - 15, bx + 15, by + 15], fill=(50, 100, 150))
            draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(100, 150, 200))
    elif theme == "train":
        _draw_grass(draw, W, H)
        draw.rectangle([0, H - 50, W, H], fill=(100, 100, 100))
        for i in range(10):
            rx = i * (W // 10)
            ry = H - 50
            draw.rectangle([rx, ry, rx + 5, ry + 5], fill=(150, 150, 150))
        _draw_clouds(draw, W, H)
        _draw_sun(draw, W, H)
        _draw_train(draw, W // 2, H // 2 + 150, 100)
    elif theme == "cat":
        _draw_grass(draw, W, H)
        _draw_flowers(draw, W, H)
        _draw_balloons(draw, W, H, 3)
        _draw_sun(draw, W, H)
        cat_color = (200, 150, 100)
        cx, cy = W // 2, H // 2 + 80
        draw.ellipse([cx - 70, cy - 50, cx + 70, cy + 60], fill=cat_color)
        draw.ellipse([cx - 45, cy - 90, cx + 45, cy - 10], fill=cat_color)
        draw.polygon([(cx - 50, cy - 70), (cx - 80, cy - 120), (cx - 20, cy - 80)], fill=cat_color)
        draw.polygon([(cx + 50, cy - 70), (cx + 80, cy - 120), (cx + 20, cy - 80)], fill=cat_color)
        draw.ellipse([cx - 15, cy - 30, cx - 5, cy - 15], fill=(100, 200, 100))
        draw.ellipse([cx + 5, cy - 30, cx + 15, cy - 15], fill=(100, 200, 100))
        draw.ellipse([cx - 20, cy - 15, cx - 8, cy - 3], fill=(0, 0, 0))
        draw.ellipse([cx + 8, cy - 15, cx + 20, cy - 3], fill=(0, 0, 0))
        draw.ellipse([cx - 6, cy + 5, cx + 6, cy + 15], fill=(255, 150, 150))
        for i in range(6):
            wx = cx - 30 + i * 12
            wy = cy + 50
            draw.line([(wx, wy), (wx + 5, wy + 20)], fill=(200, 150, 100), width=3)
    elif theme == "morning":
        _draw_grass(draw, W, H)
        _draw_flowers(draw, W, H)
        _draw_clouds(draw, W, H)
        _draw_sun(draw, W, H)
        draw.rectangle([W // 2 - 60, H // 2 + 50, W // 2 + 60, H // 2 + 150], fill=(150, 100, 50))
        draw.polygon([(W // 2 - 80, H // 2 + 50), (W // 2, H // 2), (W // 2 + 80, H // 2 + 50)], fill=(200, 50, 50))
        draw.rectangle([W // 2 - 20, H // 2 + 80, W // 2 + 20, H // 2 + 120], fill=(255, 200, 100))
        draw.rectangle([W // 2 - 15, H // 2 + 120, W // 2 - 5, H // 2 + 150], fill=(100, 80, 50))
        draw.rectangle([W // 2 + 5, H // 2 + 120, W // 2 + 15, H // 2 + 150], fill=(100, 80, 50))

    ground_y = int(H * 0.85)
    draw.rectangle([0, ground_y, W, H], fill=(60, 160, 60, 60))

    return img


def create_kids_song_video(song_data, output_path, voice_path=None, W=1080, H=1920):
    lyrics = song_data["lyrics"]
    theme = song_data.get("theme", "rainbow")
    scene_duration = 10
    clips = []
    line_groups = []
    group_size = max(1, len(lyrics) // 6)
    for i in range(0, len(lyrics), group_size):
        group = lyrics[i:i + group_size]
        if any(l.strip() for l in group):
            line_groups.append(group)

    for gi, group in enumerate(line_groups):
        img = create_scene(theme, len(group), W, H)
        scene_path = output_path.replace(".mp4", f"_scene{gi}.png")
        draw = ImageDraw.Draw(img)

        box_h = 60 * len([l for l in group if l.strip()]) + 40
        box_y = H - box_h - 80
        draw.rectangle([40, box_y, W - 40, box_y + box_h], fill=(0, 0, 0, 160))

        font = _get_font(48)
        y_offset = box_y + 20
        for line in group:
            if not line.strip():
                y_offset += 30
                continue
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            x_pos = (W - tw) // 2
            draw.text((x_pos + 2, y_offset + 2), line, fill=(0, 0, 0), font=font)
            draw.text((x_pos, y_offset), line, fill=(255, 255, 255), font=font)
            y_offset += 60

        draw.rectangle([0, 0, W, 12], fill=(255, 200, 50))
        draw.rectangle([0, H - 12, W, H], fill=(255, 200, 50))

        font_small = _get_font(32)
        subscribe_text = "SUBSCRIBE ♥"
        bbox_sub = draw.textbbox((0, 0), subscribe_text, font=font_small)
        tw_sub = bbox_sub[2] - bbox_sub[0]
        draw.text((W - tw_sub - 20, 20), subscribe_text, fill=(255, 255, 255), font=font_small)

        img.save(scene_path, quality=95)

        clip = ImageClip(scene_path, duration=scene_duration)
        clip = clip.with_effects([FadeIn(0.5), FadeOut(0.5)])
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")

    if voice_path and os.path.exists(voice_path) and os.path.getsize(voice_path) > 1000:
        audio = AudioFileClip(voice_path)
        if audio.duration < video.duration:
            from moviepy.audio.AudioClip import AudioArrayClip
            import numpy as np
            silence = np.zeros((int((video.duration - audio.duration) * 44100), 2))
            silence_clip = AudioArrayClip(silence, fps=44100).with_duration(video.duration - audio.duration)
            from moviepy.audio.CompositeAudioClip import CompositeAudioClip
            audio = CompositeAudioClip([audio.with_duration(video.duration), silence_clip.with_start(audio.duration)])
        video = video.with_audio(audio)

    video.write_videofile(output_path, fps=24, codec="libx264", preset="fast", threads=4, logger=None)

    for gi in range(len(line_groups)):
        p = output_path.replace(".mp4", f"_scene{gi}.png")
        if os.path.exists(p):
            os.remove(p)

    thumb_path = output_path.replace(".mp4", "_thumb.jpg")
    thumb = create_scene(theme, 4, W, H)
    draw = ImageDraw.Draw(thumb)
    title = song_data.get("title", "Kids Song")
    font_large = _get_font(72)
    bbox = draw.textbbox((0, 0), title, font=font_large)
    tw = bbox[2] - bbox[0]
    draw.rectangle([(W - tw) // 2 - 20, 250, (W + tw) // 2 + 20, 350], fill=(0, 0, 0, 180))
    draw.text(((W - tw) // 2, 260), title, fill=(255, 255, 255), font=font_large)
    thumb.save(thumb_path, quality=90)

    return output_path, thumb_path
