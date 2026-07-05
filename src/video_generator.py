import os
import random
import math
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    ColorClip, TextClip, AudioFileClip,
    CompositeVideoClip, concatenate_videoclips
)
from moviepy.audio.fx import AudioFadeIn, AudioFadeOut
from src.config import Config


def _get_font(size):
    fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for path in fonts:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def _make_gradient_frame(W, H, style=0, frame=0):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    palettes = [
        ((0, 20, 60), (0, 80, 180), (255, 215, 0)),
        ((60, 0, 0), (180, 20, 20), (255, 255, 200)),
        ((0, 40, 20), (0, 100, 60), (200, 255, 200)),
        ((40, 0, 60), (100, 0, 120), (255, 200, 255)),
        ((20, 20, 40), (60, 60, 100), (255, 200, 100)),
    ]
    pal = palettes[style % len(palettes)]
    for y in range(H):
        ratio = y / H
        r = int(pal[0][0] + (pal[1][0] - pal[0][0]) * ratio)
        g = int(pal[0][1] + (pal[1][1] - pal[0][1]) * ratio)
        b = int(pal[0][2] + (pal[1][2] - pal[0][2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    accent = pal[2]
    for i in range(8):
        x = int(W * 0.1 + i * W * 0.1 + 20 * math.sin(frame * 0.05 + i))
        y = int(H * 0.1 + i * H * 0.1 + 15 * math.cos(frame * 0.07 + i * 0.5))
        sz = 30 + 10 * math.sin(frame * 0.03 + i)
        draw.ellipse([x - sz, y - sz, x + sz, y + sz], fill=(accent[0], accent[1], accent[2], 40))
    draw.rectangle([0, 0, W, 5], fill=accent)
    draw.rectangle([0, H - 5, W, H], fill=accent)
    draw.rectangle([0, 0, 5, H], fill=accent)
    draw.rectangle([W - 5, 0, W, H], fill=accent)
    return img


def _wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = current + " " + word if current else word
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _create_text_scene(passages, style, W=1920, H=1080, fps=24, duration=10):
    frames = []
    total_frames = int(duration * fps)
    font_large = _get_font(56)
    font_medium = _get_font(40)
    font_small = _get_font(28)
    font_ticker = _get_font(24)
    for f in range(total_frames):
        img = _make_gradient_frame(W, H, style, f)
        draw = ImageDraw.Draw(img)
        for i, passage in enumerate(passages[:3]):
            delay = int(fps * i * 1.5)
            if f >= delay:
                alpha = min(1.0, (f - delay) / 15)
                lines = _wrap_text(passage, font_large, W - 200, draw)
                y_start = 150 + i * 300
                for li, line in enumerate(lines):
                    bbox = draw.textbbox((0, 0), line, font=font_large)
                    x_off = int(50 * (1 - alpha))
                    x_pos = 100 + x_off
                    y_pos = y_start + li * 60
                    draw.text((x_pos + 2, y_pos + 2), line, fill=(0, 0, 0), font=font_large)
                    draw.text((x_pos, y_pos), line, fill=(255, 255, 255, int(255 * alpha)), font=font_large)
        scroll_x = W - int(f * 8) % (W + 1000)
        draw.text((scroll_x, H - 40), "FOOTBALL VIRAL | FOLLOW FOR MORE | SUBSCRIBE | SHARE | LIKE", fill=(255, 215, 0), font=font_ticker)
        draw.text((20, H - 80), "FOOTBALL VIRAL", fill=(255, 215, 0), font=font_small)
        progress = f"{int(f / fps)}s"
        draw.text((W - 100, 20), progress, fill=(200, 200, 200), font=font_small)
        frame_path = f"/tmp/fifa_scene_{style}_{f}.png"
        img.save(frame_path, quality=92)
        frames.append(frame_path)
    return frames


STYLES = ["classic", "breaking", "sports", "worldcup", "analysis", "news", "premium"]


def create_video(script_data, output_path, style=None):
    if style is None:
        style = random.choice(STYLES)
    W, H = 1920, 1080
    script = script_data.get("script", "")
    sentences = [s.strip() for s in script.replace("\n\n", "\n").split("\n") if s.strip()]
    passages = []
    for s in sentences:
        if len(s) > 200:
            parts = [s[i:i+150] for i in range(0, len(s), 150)]
            passages.extend(parts)
        else:
            passages.append(s)
    total_dur = max(30, len(passages) * 4)
    voice_path = output_path.replace(".mp4", "_voice.mp3")
    if not os.path.exists(voice_path):
        try:
            import edge_tts
            import asyncio
            import re
            text = script.replace("\n", " ")
            text = re.sub(r'([.!?])\s+', r'\1 <break time="400ms"/> ', text)
            async def _run():
                tts = edge_tts.Communicate(text, voice="en-US-GuyNeural", rate="-5%", pitch="0Hz")
                await tts.save(voice_path)
            asyncio.run(_run())
        except Exception:
            voice_path = None
    if voice_path and os.path.exists(voice_path) and os.path.getsize(voice_path) > 1000:
        try:
            audio = AudioFileClip(voice_path)
            total_dur = max(audio.duration + 2, 30)
        except Exception:
            pass
    style_idx = STYLES.index(style) if style in STYLES else 0
    fps = 24
    all_frames = _create_text_scene(passages, style_idx, W, H, fps, total_dur)
    from moviepy import ImageClip
    clips = []
    chunk = max(1, len(all_frames) // 10)
    for i in range(0, len(all_frames), chunk):
        segment = all_frames[i:i + chunk]
        if not segment:
            continue
        seg_dur = len(segment) / fps
        clip = ImageClip(segment[0], duration=seg_dur)
        clips.append(clip)
    if not clips:
        fallback = ColorClip(color=(0, 20, 60), size=(W, H), duration=5)
        clips = [fallback]
    video = concatenate_videoclips(clips, method="compose")
    if voice_path and os.path.exists(voice_path) and os.path.getsize(voice_path) > 1000:
        try:
            audio = AudioFileClip(voice_path)
            video = video.with_audio(audio)
        except Exception:
            pass
    video.write_videofile(output_path, fps=fps, codec="libx264", preset="fast", threads=4, logger=None)
    for fp in all_frames:
        if os.path.exists(fp):
            os.remove(fp)
    if voice_path and os.path.exists(voice_path):
        os.remove(voice_path)
    thumb_path = output_path.replace(".mp4", "_thumb.jpg")
    thumb = _make_gradient_frame(1280, 720, style_idx, 0)
    draw = ImageDraw.Draw(thumb)
    title = script_data.get("title", "Football Viral")
    font_large = _get_font(56)
    bbox = draw.textbbox((0, 0), title, font=font_large)
    tw = bbox[2] - bbox[0]
    draw.rectangle([(1280 - tw) // 2 - 20, 300, (1280 + tw) // 2 + 20, 380], fill=(0, 0, 0, 200))
    draw.text(((1280 - tw) // 2, 310), title, fill=(255, 255, 255), font=font_large)
    thumb.save(thumb_path, quality=90)
    return output_path, thumb_path


def create_thumbnail(title, output_path, style=None):
    if style is None:
        style = random.choice(STYLES)
    style_idx = STYLES.index(style) if style in STYLES else 0
    thumb = _make_gradient_frame(1280, 720, style_idx, 0)
    draw = ImageDraw.Draw(thumb)
    font_large = _get_font(56)
    bbox = draw.textbbox((0, 0), title, font=font_large)
    tw = bbox[2] - bbox[0]
    draw.rectangle([(1280 - tw) // 2 - 20, 300, (1280 + tw) // 2 + 20, 380], fill=(0, 0, 0, 200))
    draw.text(((1280 - tw) // 2, 310), title, fill=(255, 255, 255), font=font_large)
    thumb.save(output_path, quality=90)
    return output_path
