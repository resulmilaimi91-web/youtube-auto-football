import os
import textwrap
import random
import traceback
import sys
import urllib.request
import json

from moviepy import (
    VideoFileClip, ColorClip, TextClip, AudioFileClip,
    CompositeVideoClip, CompositeAudioClip, afx, ImageClip,
    concatenate_videoclips
)
from PIL import Image, ImageDraw, ImageFont
from src.config import Config


def _get_font(size):
    fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        "arial.ttf", "Arial.ttf", "Arial Bold.ttf",
    ]
    for path in fonts:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def generate_voiceover(script_text, output_path):
    try:
        import edge_tts
        import asyncio
        voices = ["en-US-GuyNeural", "en-US-JennyNeural", "en-GB-RyanNeural", "en-US-TonyNeural", "en-AU-WilliamNeural"]
        voice = random.choice(voices)
        async def _run():
            tts = edge_tts.Communicate(script_text, voice=voice, rate="-2%", pitch="+0Hz", volume="+25%")
            await tts.save(output_path)
        asyncio.run(_run())
        if os.path.getsize(output_path) > 1000:
            return
    except Exception as e:
        print(f"edge-tts failed: {e}")

    try:
        from gtts import gTTS
        tts = gTTS(text=script_text, lang="en", slow=False, tld="com")
        tts.save(output_path)
        if os.path.getsize(output_path) > 1000:
            return
    except Exception as e2:
        print(f"gTTS failed: {e2}")
        with open(output_path, "wb") as f:
            f.write(b"")


def _download_image(url, path):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=10).read()
        if len(data) > 5000:
            with open(path, "wb") as f:
                f.write(data)
            return True
    except Exception:
        pass
    return False


def download_football_images(count=5):
    paths = []
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    queries = [
        "football+stadium+night",
        "soccer+players+action",
        "world+cup+trophy",
        "football+fans+celebration",
        "soccer+goal+net",
    ]
    for i in range(min(count, len(queries))):
        path = os.path.join(Config.OUTPUT_DIR, f"scene_{i}.jpg")
        ok = _download_image(f"https://source.unsplash.com/1920x1080/?{queries[i]}&sig={random.randint(1,99999)}", path)
        if not ok:
            ok = _download_image(f"https://picsum.photos/1920/1080?random={random.randint(1,99999)}", path)
        if ok:
            paths.append(path)
    return paths


def _make_gradient_bg(W, H, style=0):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    if style == 0:
        c1, c2, c3 = (10, 15, 35), (20, 40, 80), (5, 10, 25)
    elif style == 1:
        c1, c2, c3 = (25, 10, 10), (60, 15, 15), (15, 5, 5)
    elif style == 2:
        c1, c2, c3 = (10, 25, 10), (15, 60, 15), (5, 15, 5)
    elif style == 3:
        c1, c2, c3 = (20, 15, 30), (40, 20, 60), (10, 8, 15)
    else:
        c1, c2, c3 = (15, 20, 30), (30, 45, 70), (8, 12, 20)

    for y in range(H):
        r = int(c1[0] + (c2[0] - c1[0]) * y / H)
        g = int(c1[1] + (c2[1] - c1[1]) * y / H)
        b = int(c1[2] + (c2[2] - c1[2]) * y / H)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    return img


STYLES = ["classic", "breaking", "sports", "worldcup", "analysis"]


def create_thumbnail(title, output_path, style=None):
    W, H = 1280, 720
    if style is None:
        style = random.choice(STYLES)

    style_idx = STYLES.index(style) if style in STYLES else 0
    bg = _make_gradient_bg(W, H, style_idx)
    draw = ImageDraw.Draw(bg)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    if style == "breaking":
        od.rectangle([0, 0, W, 80], fill=(255, 0, 0, 230))
        od.rectangle([0, H - 80, W, H], fill=(255, 0, 0, 230))
    elif style == "sports":
        od.rectangle([0, H - 120, W, H], fill=(0, 0, 0, 200))
        od.rectangle([0, 0, 120, H], fill=(255, 200, 0, 100))
    elif style == "worldcup":
        od.rectangle([0, H - 100, W, H], fill=(0, 50, 120, 220))
        od.rectangle([0, 0, W, 80], fill=(0, 50, 120, 220))
    elif style == "analysis":
        od.rectangle([0, 0, W, 60], fill=(20, 20, 20, 200))
        od.rectangle([0, H - 60, W, H], fill=(20, 20, 20, 200))
    else:
        od.rectangle([0, 400, W, H], fill=(0, 0, 0, 180))

    bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(bg)

    font = _get_font(56)
    small_font = _get_font(28)

    lines = textwrap.wrap(title, width=18)
    y = 140
    for line in lines[:3]:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (W - tw) // 2
        draw.text((x + 2, y + 2), line, fill=(0, 0, 0), font=font)
        draw.text((x, y), line, fill=(255, 255, 255), font=font)
        y += 70

    if style == "breaking":
        draw.rectangle([0, 0, W, 80], fill=(255, 0, 0))
        draw.text((W // 2 - 100, 20), "BREAKING NEWS", fill=(255, 255, 255), font=_get_font(36))
        draw.rectangle([0, H - 80, W, H], fill=(255, 0, 0))
        draw.text((W // 2 - 80, H - 60), "SUBSCRIBE NOW", fill=(255, 255, 255), font=small_font)
    elif style == "worldcup":
        draw.rectangle([0, 0, W, 80], fill=(0, 50, 120))
        draw.text((W // 2 - 120, 20), "FIFA WORLD CUP 2026", fill=(255, 215, 0), font=_get_font(32))
        draw.rectangle([0, H - 100, W, H], fill=(0, 50, 120))
        draw.text((W // 2 - 80, H - 60), "SUBSCRIBE NOW", fill=(255, 255, 255), font=small_font)
    elif style == "analysis":
        draw.rectangle([0, 0, W, 60], fill=(30, 30, 30))
        draw.text((40, 15), "ANALYSIS", fill=(255, 200, 0), font=_get_font(30))
        draw.rectangle([0, H - 60, W, H], fill=(30, 30, 30))
        draw.text((W // 2 - 80, H - 45), "SUBSCRIBE NOW", fill=(255, 255, 255), font=small_font)
    else:
        badge = Image.new("RGBA", (240, 50), (255, 0, 0, 255))
        bg.paste(badge, (W // 2 - 120, H - 90), badge)
        b_draw = ImageDraw.Draw(bg)
        b_draw.text((W // 2 - 85, H - 82), "SUBSCRIBE", fill=(255, 255, 255), font=small_font)

    bg.save(output_path, quality=92)
    return output_path


def create_video(script_data, output_path, style=None):
    VOICE_PATH = os.path.join(Config.OUTPUT_DIR, "voiceover.mp3")
    THUMB_PATH = os.path.join(Config.OUTPUT_DIR, "thumbnail.jpg")
    BG_PATH = os.path.join(Config.ASSETS_DIR, "background.mp4")
    MUSIC_PATH = os.path.join(Config.ASSETS_DIR, "music.mp3")

    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

    generate_voiceover(script_data["script"], VOICE_PATH)

    if style is None:
        style = random.choice(STYLES)
    create_thumbnail(script_data["title"], THUMB_PATH, style)

    audio = AudioFileClip(VOICE_PATH)
    duration = audio.duration + 3

    W, H = Config.VIDEO_WIDTH, Config.VIDEO_HEIGHT

    img_paths = download_football_images(5)
    scenes = []
    if img_paths:
        seg_dur = duration / len(img_paths)
        for i, p in enumerate(img_paths):
            try:
                clip = ImageClip(p, duration=seg_dur).resized((W, H))
                fade = min(0.5, seg_dur * 0.15)
                clip = clip.with_effects([afx.FadeIn(fade), afx.FadeOut(fade)])
                scenes.append(clip)
            except Exception:
                pass

    if not scenes:
        bg_clip = ColorClip(size=(W, H), color=(10, 15, 30), duration=duration)
        scenes = [bg_clip]

    try:
        bg_video = concatenate_videoclips(scenes, method="compose")
    except Exception:
        bg_video = scenes[0].with_duration(duration)

    font_path = None
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "arial.ttf", "Arial.ttf"]:
        if os.path.exists(f):
            font_path = f
            break
    if not font_path and sys.platform == "linux":
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    overlays = []

    if style == "breaking":
        bar = ColorClip(size=(W, 70), color=(255, 0, 0), duration=duration).with_position((0, 0))
        bar_text = TextClip(text="BREAKING NEWS", font_size=32, color="white", font=font_path).with_position(("center", 18)).with_duration(duration)
        bottom_bar = ColorClip(size=(W, 60), color=(0, 0, 0), duration=duration).with_position((0, H - 60)).with_effects([afx.MultiplyVolume(0)])
        bottom_text = TextClip(text="SUBSCRIBE FOR MORE NEWS", font_size=26, color="white", font=font_path).with_position(("center", H - 48)).with_duration(duration)
        overlays.extend([bar, bar_text, bottom_bar, bottom_text])
    elif style == "worldcup":
        top_bar = ColorClip(size=(W, 70), color=(0, 50, 120), duration=duration).with_position((0, 0))
        top_text = TextClip(text="FIFA WORLD CUP 2026", font_size=32, color=(255, 215, 0), font=font_path).with_position(("center", 18)).with_duration(duration)
        bottom_bar = ColorClip(size=(W, 50), color=(0, 50, 120), duration=duration).with_position((0, H - 50)).with_effects([afx.MultiplyVolume(0)])
        bottom_text = TextClip(text="SUBSCRIBE NOW", font_size=24, color="white", font=font_path).with_position(("center", H - 40)).with_duration(duration)
        overlays.extend([top_bar, top_text, bottom_bar, bottom_text])
    elif style == "sports":
        side_bar = ColorClip(size=(8, H), color=(255, 200, 0), duration=duration).with_position((0, 0))
        bottom_bar = ColorClip(size=(W, 50), color=(0, 0, 0), duration=duration).with_position((0, H - 50)).with_effects([afx.MultiplyVolume(0)])
        bottom_text = TextClip(text="FOOTBALL HIGHLIGHTS DAILY", font_size=24, color="white", font=font_path).with_position(("center", H - 40)).with_duration(duration)
        overlays.extend([side_bar, bottom_bar, bottom_text])
    elif style == "analysis":
        top_bar = ColorClip(size=(W, 50), color=(20, 20, 20), duration=duration).with_position((0, 0))
        top_text = TextClip(text="TACTICAL ANALYSIS", font_size=28, color=(255, 200, 0), font=font_path).with_position((30, 10)).with_duration(duration)
        bottom_bar = ColorClip(size=(W, 40), color=(20, 20, 20), duration=duration).with_position((0, H - 40)).with_effects([afx.MultiplyVolume(0)])
        overlays.extend([top_bar, top_text, bottom_bar])
    else:
        ticker = ColorClip(size=(W, 40), color=(255, 0, 0), duration=duration).with_position((0, H - 40)).with_effects([afx.MultiplyVolume(0)])
        ticker_text = TextClip(text="FOOTBALL HIGHLIGHTS DAILY - SUBSCRIBE!", font_size=20, color="white", font=font_path).with_position(("center", H - 32)).with_duration(duration)
        overlays.extend([ticker, ticker_text])

    title_clip = TextClip(
        text=script_data["title"],
        font_size=Config.TITLE_FONT_SIZE,
        color="white",
        font=font_path,
        text_align="center",
        size=(W - 200, None),
        method="caption",
    ).with_position(("center", int(H * 0.35))).with_duration(duration)

    shadow = TextClip(
        text=script_data["title"],
        font_size=Config.TITLE_FONT_SIZE,
        color=(0, 0, 0),
        font=font_path,
        text_align="center",
        size=(W - 200, None),
        method="caption",
    ).with_position(("center", int(H * 0.35) + 3)).with_duration(duration).with_opacity(0.5)

    subscribe = TextClip(
        text="SUBSCRIBE",
        font_size=32,
        color=(255, 215, 0),
        font=font_path,
    ).with_position(("center", int(H * 0.82))).with_duration(duration)

    if os.path.exists(MUSIC_PATH):
        music = AudioFileClip(MUSIC_PATH).with_duration(duration).with_effects([afx.MultiplyVolume(0.08)])
        final_audio = CompositeAudioClip([audio, music])
    else:
        final_audio = audio

    all_clips = [bg_video, shadow, title_clip, subscribe] + overlays
    video = CompositeVideoClip(all_clips).with_audio(final_audio)

    video.write_videofile(
        output_path,
        fps=Config.FPS,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=2,
        ffmpeg_params=["-crf", "26"],
    )

    video.close()
    audio.close()
    for p in img_paths:
        if os.path.exists(p):
            os.remove(p)
    if os.path.exists(VOICE_PATH):
        os.remove(VOICE_PATH)

    return output_path, THUMB_PATH
