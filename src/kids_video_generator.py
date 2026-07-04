import os
import random
import math
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx import FadeIn, FadeOut
from moviepy.audio.fx import AudioFadeIn, AudioFadeOut


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


def _create_scene_bg(seed):
    W, H = 1080, 1920
    palettes = [
        (100, 180, 255), (255, 150, 100), (180, 100, 255), (50, 200, 200),
        (255, 200, 100), (150, 255, 150), (255, 150, 200), (200, 200, 100),
    ]
    pal = palettes[seed % len(palettes)]
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        r = int(pal[0] + (pal[0] // 2) * ratio)
        g = int(pal[1] + (pal[1] // 2) * ratio)
        b = int(pal[2] + (pal[2] // 2) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    ground_y = int(H * 0.75)
    draw.rectangle([0, ground_y, W, H], fill=(pal[0] // 2, pal[1] + 50, pal[2] // 2))
    for _ in range(5):
        cx = random.randint(100, W - 100)
        cy = random.randint(80, ground_y - 100)
        s = random.randint(60, 140)
        draw.ellipse([cx - s, cy - s // 2, cx + s, cy + s // 2], fill=(255, 255, 255, 80))
    for _ in range(4):
        cx = random.randint(80, W - 80)
        cy = random.randint(ground_y + 30, H - 40)
        rsize = random.randint(35, 75)
        fc = random.choice([(255, 100, 100), (255, 255, 100), (100, 255, 100)])
        draw.ellipse([cx - rsize, cy - rsize // 2, cx + rsize, cy + rsize // 2], fill=fc)
        draw.ellipse([cx - 4, cy - 6, cx + 4, cy + 4], fill=(255, 200, 50))
    return img


def create_kids_video(script_data, output_path, style=None, voice_path=None):
    W, H = 1080, 1920
    scene_duration = 15
    num_scenes = 8
    clips = []
    for i in range(num_scenes):
        bg = _create_scene_bg(i)
        bg_path = output_path.replace(".mp4", f"_scene{i}.png")
        draw = ImageDraw.Draw(bg)
        cx, cy = W // 2, H // 2 + 50
        draw.ellipse([cx - 120, cy - 120, cx + 120, cy + 120], fill=(0, 0, 0, 120))
        draw.ellipse([cx - 115, cy - 115, cx + 115, cy + 115], outline=(255, 215, 0), width=5)
        px, py = cx - 40, cy - 60
        draw.polygon([(px, py), (px, py + 120), (px + 80, py + 60)], fill=(255, 215, 0))
        draw.rectangle([0, 0, W, 8], fill=(255, 215, 0))
        draw.rectangle([0, H - 8, W, H], fill=(255, 215, 0))
        draw.rectangle([W // 2 - 200, H - 160, W // 2 + 200, H - 100], fill=(0, 0, 0))
        bbox_sub = draw.textbbox((0, 0), "SUBSCRIBE", font=_get_font(70))
        tw = bbox_sub[2] - bbox_sub[0]
        draw.text((W // 2 - tw // 2, H - 150), "SUBSCRIBE", fill=(255, 215, 0), font=_get_font(70))
        bg.save(bg_path, quality=95)
        clip = ImageClip(bg_path, duration=scene_duration)
        clip = clip.with_effects([FadeIn(0.5), FadeOut(0.5)])
        clips.append(clip)
    video = concatenate_videoclips(clips, method="compose")
    if voice_path and os.path.exists(voice_path) and os.path.getsize(voice_path) > 1000:
        audio = AudioFileClip(voice_path)
        video = video.with_audio(audio)
    video.write_videofile(output_path, fps=24, codec="libx264", preset="fast", threads=4, logger=None)
    for i in range(num_scenes):
        p = output_path.replace(".mp4", f"_scene{i}.png")
        if os.path.exists(p):
            os.remove(p)
    thumb_path = output_path.replace(".mp4", "_thumb.jpg")
    bg = _create_scene_bg(0)
    bg.save(thumb_path, quality=90)
    return output_path, thumb_path
