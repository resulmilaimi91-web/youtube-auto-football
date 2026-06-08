import os
import textwrap
import random
import traceback
import sys
import urllib.request

from moviepy import (
    VideoFileClip, ColorClip, TextClip, AudioFileClip,
    CompositeVideoClip, CompositeAudioClip, afx, ImageClip
)
from PIL import Image, ImageDraw, ImageFont
from src.config import Config


def _get_font(size):
    fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        "arial.ttf",
        "Arial.ttf",
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

        voices = ["en-US-GuyNeural", "en-US-JennyNeural", "en-GB-RyanNeural", "en-US-TonyNeural"]
        voice = random.choice(voices)

        async def _run():
            tts = edge_tts.Communicate(
                script_text,
                voice=voice,
                rate="+0%",
                pitch="+0Hz",
                volume="+20%",
            )
            await tts.save(output_path)

        asyncio.run(_run())
        if os.path.getsize(output_path) > 1000:
            return
    except Exception as e:
        print(f"edge-tts failed ({e}), falling back to gTTS...")

    try:
        from gtts import gTTS
        tts = gTTS(text=script_text, lang="en", slow=False, tld="com")
        tts.save(output_path)
        if os.path.getsize(output_path) > 1000:
            return
    except Exception as e2:
        print(f"gTTS failed too ({e2}), continuing without voice...")
        with open(output_path, "wb") as f:
            f.write(b"")


def download_images(count=4):
    paths = []
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    keywords = ["football+stadium", "soccer+goal", "world+cup+trophy", "football+players"]
    for i in range(min(count, len(keywords))):
        try:
            url = f"https://source.unsplash.com/1920x1080/?{keywords[i]}"
            path = os.path.join(Config.OUTPUT_DIR, f"img_{i}.jpg")
            urllib.request.urlretrieve(url, path)
            if os.path.getsize(path) > 5000:
                paths.append(path)
        except Exception:
            pass
    return paths


def create_thumbnail(title, output_path):
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), (10, 15, 30))
    draw = ImageDraw.Draw(img)

    for y in range(H):
        r = int(10 + (220 - 10) * y / H)
        g = int(15 + (180 - 15) * y / H)
        b = int(30 + (0 - 30) * y / H)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    o_draw = ImageDraw.Draw(overlay)
    o_draw.rectangle([0, 400, W, H], fill=(0, 0, 0, 200))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    font = _get_font(56)
    small_font = _get_font(30)

    lines = textwrap.wrap(title, width=16)
    y = 130
    for line in lines[:3]:
        draw.text((40, y), line, fill=(255, 255, 255), font=font)
        y += 65

    draw.rectangle([(20, 110), (25, 110 + (y - 130))], fill=(255, 200, 0))
    draw.rectangle([(20, 470), (W - 20), 472], fill=(255, 200, 0))

    badge = Image.new("RGBA", (240, 50), (255, 0, 0, 255))
    img.paste(badge, (W // 2 - 120, H - 90), badge)
    b_draw = ImageDraw.Draw(img)
    b_draw.text((W // 2 - 85, H - 82), "SUBSCRIBE", fill=(255, 255, 255), font=small_font)

    img.save(output_path, quality=92)
    return output_path


def create_video(script_data, output_path):
    VOICE_PATH = os.path.join(Config.OUTPUT_DIR, "voiceover.mp3")
    THUMB_PATH = os.path.join(Config.OUTPUT_DIR, "thumbnail.jpg")
    BG_PATH = os.path.join(Config.ASSETS_DIR, "background.mp4")
    MUSIC_PATH = os.path.join(Config.ASSETS_DIR, "music.mp3")

    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

    generate_voiceover(script_data["script"], VOICE_PATH)

    create_thumbnail(script_data["title"], THUMB_PATH)

    audio = AudioFileClip(VOICE_PATH)
    duration = audio.duration + 3

    W, H = Config.VIDEO_WIDTH, Config.VIDEO_HEIGHT

    img_paths = download_images(4)
    scenes = []
    if img_paths:
        seg_dur = duration / len(img_paths)
        for i, p in enumerate(img_paths):
            try:
                clip = ImageClip(p, duration=seg_dur).resized((W, H))
                scenes.append(clip)
            except Exception:
                pass
    else:
        pass

    if not scenes:
        if os.path.exists(BG_PATH):
            bg = VideoFileClip(BG_PATH).with_duration(duration).resized((W, H))
            scenes = [bg]
        else:
            bg = ColorClip(size=(W, H), color=(10, 15, 30), duration=duration)
            scenes = [bg]

    font_path = None
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "arial.ttf", "Arial.ttf"]:
        if os.path.exists(f):
            font_path = f
            break
    if not font_path and sys.platform == "linux":
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    news_bar = ColorClip(
        size=(W, 50), color=(255, 0, 0), duration=duration
    ).with_position((0, H - 100))

    news_ticker = TextClip(
        text="FOOTBALL HIGHLIGHTS DAILY - WORLD CUP 2026 - SUBSCRIBE!",
        font_size=24,
        color="white",
        font=font_path,
    ).with_position((20, H - 92)).with_duration(duration)

    overlay = TextClip(
        text=script_data["title"],
        font_size=Config.TITLE_FONT_SIZE,
        color="white",
        font=font_path,
        text_align="center",
        size=(W - 120, None),
        method="caption",
    ).with_position("center").with_duration(duration)

    date_str = script_data["description"].split("\n")[0][:30] if "\n" in script_data["description"] else ""
    date_clip = TextClip(
        text="Latest Football News",
        font_size=Config.SUBTITLE_FONT_SIZE,
        color="#FFD700",
        font=font_path,
        text_align="center",
    ).with_position(("center", int(H * 0.08))).with_duration(duration)

    footer = TextClip(
        text="SUBSCRIBE NOW",
        font_size=Config.FOOTER_FONT_SIZE,
        color="yellow",
        font=font_path,
    ).with_position(("center", H - 50)).with_duration(duration)

    if os.path.exists(MUSIC_PATH):
        music = AudioFileClip(MUSIC_PATH).with_duration(duration).with_effects([afx.MultiplyVolume(0.08)])
        final_audio = CompositeAudioClip([audio, music])
    else:
        final_audio = audio

    combined = CompositeVideoClip([*scenes, news_bar, news_ticker, overlay, date_clip, footer]).with_audio(final_audio)

    combined.write_videofile(
        output_path,
        fps=Config.FPS,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=2,
        ffmpeg_params=["-crf", "26"],
    )

    combined.close()
    audio.close()
    for p in img_paths:
        if os.path.exists(p):
            os.remove(p)
    if os.path.exists(VOICE_PATH):
        os.remove(VOICE_PATH)

    return output_path, THUMB_PATH
