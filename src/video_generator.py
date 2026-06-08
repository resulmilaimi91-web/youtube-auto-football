import os
import asyncio
import textwrap
import random
import traceback

from moviepy import (
    VideoFileClip, ColorClip, TextClip, AudioFileClip,
    CompositeVideoClip, CompositeAudioClip, afx
)
from PIL import Image, ImageDraw, ImageFont
from src.config import Config

def generate_voiceover(script_text, output_path):
    try:
        import edge_tts
        voice = random.choice(["sq-AL-IlirNeural", "sq-AL-AnilaNeural"])
        async def _run():
            tts = edge_tts.Communicate(script_text, voice=voice, rate="+10%")
            await tts.save(output_path)
        asyncio.run(_run())
        if os.path.getsize(output_path) > 1000:
            return
    except Exception:
        traceback.print_exc()

    from gtts import gTTS
    tts = gTTS(text=script_text, lang="sq", slow=False)
    tts.save(output_path)

def create_thumbnail(title, output_path):
    img = Image.new("RGB", (1280, 720), (20, 30, 48))

    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 60)
        small_font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    draw.rectangle([0, 500, 1280, 720], fill=(255, 200, 0))
    draw.text((40, 40), "⚽", fill=(255, 255, 255), font=font)

    lines = textwrap.wrap(title, width=15)
    y = 150
    for line in lines[:3]:
        draw.text((40, y), line, fill=(255, 255, 255), font=font)
        y += 70

    draw.text((40, 530), "ABONOHU!", fill=(0, 0, 0), font=small_font)

    img.save(output_path, quality=95)
    return output_path

def create_video(script_data, output_path):
    VOICE_PATH = os.path.join(Config.OUTPUT_DIR, "voiceover.mp3")
    THUMB_PATH = os.path.join(Config.OUTPUT_DIR, "thumbnail.jpg")
    BG_PATH = os.path.join(Config.ASSETS_DIR, "background.mp4")
    MUSIC_PATH = os.path.join(Config.ASSETS_DIR, "music.mp3")

    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

    asyncio.run(generate_voiceover(script_data["script"], VOICE_PATH))

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

    overlay = TextClip(
        text=script_data["title"],
        font_size=50,
        color="white",
        font="Arial",
        text_align="center",
        size=(Config.VIDEO_WIDTH - 80, None),
        method="caption",
    ).with_position("center").with_duration(duration)

    footer = TextClip(
        text="ABONOHU 🔔",
        font_size=40,
        color="yellow",
        font="Arial",
    ).with_position(("center", Config.VIDEO_HEIGHT - 120)).with_duration(duration)

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
