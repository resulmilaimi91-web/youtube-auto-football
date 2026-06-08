import os
import textwrap
import random
import traceback
import sys

from moviepy import (
    VideoFileClip, ColorClip, TextClip, AudioFileClip,
    CompositeVideoClip, CompositeAudioClip, afx
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

        voices = ["en-US-GuyNeural", "en-US-JennyNeural", "en-GB-RyanNeural", "en-AU-WilliamNeural"]
        voice = random.choice(voices)

        async def _run():
            tts = edge_tts.Communicate(script_text, voice=voice, rate="+5%", pitch="-2Hz")
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


def create_thumbnail(title, output_path):
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), (20, 30, 48))
    draw = ImageDraw.Draw(img)

    for y in range(H):
        r = int(20 + (235 - 20) * y / H)
        g = int(30 + (200 - 30) * y / H)
        b = int(48 + (0 - 48) * y / H)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    o_draw = ImageDraw.Draw(overlay)
    o_draw.rectangle([0, 460, W, H], fill=(0, 0, 0, 180))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    font = _get_font(58)
    small_font = _get_font(32)

    lines = textwrap.wrap(title, width=14)
    y = 140
    for line in lines[:3]:
        draw.text((50, y), line, fill=(255, 255, 255), font=font)
        y += 68

    accent = Image.new("RGBA", (8, y - 140), (255, 200, 0, 230))
    img.paste(accent, (20, 140), accent)

    draw.rectangle([(20, 485), (W - 20, 485)], fill=(255, 200, 0))

    badge = Image.new("RGBA", (220, 50), (255, 200, 0, 255))
    img.paste(badge, (W // 2 - 110, H - 100), badge)
    b_draw = ImageDraw.Draw(img)
    b_draw.text((W // 2 - 75, H - 92), "SUBSCRIBE", fill=(0, 0, 0), font=small_font)

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
    duration = audio.duration + 2

    if os.path.exists(BG_PATH):
        bg = VideoFileClip(BG_PATH).with_duration(duration).resized((Config.VIDEO_WIDTH, Config.VIDEO_HEIGHT))
    else:
        bg = ColorClip(
            size=(Config.VIDEO_WIDTH, Config.VIDEO_HEIGHT),
            color=(20, 30, 48),
            duration=duration,
        )

    font_path = None
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "arial.ttf", "Arial.ttf"]:
        if os.path.exists(f):
            font_path = f
            break
    if not font_path and sys.platform == "linux":
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    overlay = TextClip(
        text=script_data["title"],
        font_size=Config.TITLE_FONT_SIZE,
        color="white",
        font=font_path,
        text_align="center",
        size=(Config.VIDEO_WIDTH - 60, None),
        method="caption",
    ).with_position("center").with_duration(duration)

    sub_text = "Daily Football Updates"
    sub = TextClip(
        text=sub_text,
        font_size=Config.SUBTITLE_FONT_SIZE,
        color="#FFD700",
        font=font_path,
        text_align="center",
        size=(Config.VIDEO_WIDTH - 60, None),
        method="caption",
    ).with_position(("center", Config.VIDEO_HEIGHT * 0.12)).with_duration(duration)

    footer = TextClip(
        text="SUBSCRIBE",
        font_size=Config.FOOTER_FONT_SIZE,
        color="yellow",
        font=font_path,
    ).with_position(("center", Config.VIDEO_HEIGHT - 80)).with_duration(duration)

    bar_bg = ColorClip(
        size=(Config.VIDEO_WIDTH, 70),
        color=(255, 0, 0),
        duration=duration,
    ).with_position(("center", Config.VIDEO_HEIGHT - 70)).with_effects([afx.MultiplyVolume(0)]).with_opacity(0.0)

    bar_text = TextClip(
        text="SUBSCRIBE NOW",
        font_size=Config.FOOTER_FONT_SIZE,
        color="white",
        font=font_path,
    ).with_position(("center", Config.VIDEO_HEIGHT - 62)).with_duration(duration)

    if os.path.exists(MUSIC_PATH):
        music = AudioFileClip(MUSIC_PATH).with_duration(duration).with_effects([afx.MultiplyVolume(0.1)])
        final_audio = CompositeAudioClip([audio, music])
    else:
        final_audio = audio

    video = CompositeVideoClip([bg, overlay, sub, footer, bar_text]).with_audio(final_audio)

    video.write_videofile(
        output_path,
        fps=Config.FPS,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=2,
        ffmpeg_params=["-crf", "28"],
    )

    video.close()
    audio.close()
    if os.path.exists(VOICE_PATH):
        os.remove(VOICE_PATH)

    return output_path, THUMB_PATH
