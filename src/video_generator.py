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

        voice = random.choice(["en-US-GuyNeural", "en-US-JennyNeural", "en-GB-RyanNeural"])
        async def _run():
            tts = edge_tts.Communicate(script_text, voice=voice, rate="+5%")
            await tts.save(output_path)

        import asyncio
        asyncio.run(_run())
        if os.path.getsize(output_path) > 1000:
            return
    except Exception:
        traceback.print_exc()

    from gtts import gTTS
    tts = gTTS(text=script_text, lang="en", slow=False)
    tts.save(output_path)


def create_thumbnail(title, output_path):
    img = Image.new("RGB", (1280, 720), (20, 30, 48))
    draw = ImageDraw.Draw(img)
    font = _get_font(60)
    small_font = _get_font(30)

    draw.rectangle([0, 500, 1280, 720], fill=(255, 200, 0))

    lines = textwrap.wrap(title, width=15)
    y = 150
    for line in lines[:3]:
        draw.text((40, y), line, fill=(255, 255, 255), font=font)
        y += 70

    draw.text((40, 530), "SUBSCRIBE!", fill=(0, 0, 0), font=small_font)
    img.save(output_path, quality=95)
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

    video = CompositeVideoClip([bg, overlay, sub, footer]).with_audio(final_audio)

    if os.path.exists(MUSIC_PATH):
        music = AudioFileClip(MUSIC_PATH).with_duration(duration).with_effects([afx.MultiplyVolume(0.1)])
        final_audio = CompositeAudioClip([audio, music])
    else:
        final_audio = audio

    video = CompositeVideoClip([bg, overlay, footer]).with_audio(final_audio)

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
