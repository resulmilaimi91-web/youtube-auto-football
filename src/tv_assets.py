import os
import random
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    ColorClip, TextClip, CompositeVideoClip, CompositeAudioClip,
    AudioFileClip, afx, ImageClip, concatenate_videoclips
)

W, H = 1920, 1080
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")


def _get_font(size):
    fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "arial.ttf", "Arial.ttf", "Arial Bold.ttf",
    ]
    for path in fonts:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def create_logo(output_path):
    size = 400
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.ellipse([10, 10, size - 10, size - 10], fill=(20, 50, 120, 255))
    draw.ellipse([30, 30, size - 30, size - 30], fill=(0, 80, 180, 255))

    font_big = _get_font(80)
    font_small = _get_font(24)

    bbox = draw.textbbox((0, 0), "FHD", font=font_big)
    tw = bbox[2] - bbox[0]
    draw.text(((size - tw) // 2, size // 2 - 60), "FHD", fill=(255, 255, 255, 255), font=font_big)

    bbox2 = draw.textbbox((0, 0), "FOOTBALL", font=font_small)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((size - tw2) // 2, size // 2 + 30), "FOOTBALL", fill=(255, 215, 0, 255), font=font_small)

    bbox3 = draw.textbbox((0, 0), "HIGHLIGHTS", font=font_small)
    tw3 = bbox3[2] - bbox3[0]
    draw.text(((size - tw3) // 2, size // 2 + 60), "HIGHLIGHTS", fill=(255, 215, 0, 255), font=font_small)

    img.save(output_path, "PNG")
    return output_path


def create_tv_intro(output_path, duration=4):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    font_path = None
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "arial.ttf", "Arial.ttf"]:
        if os.path.exists(f):
            font_path = f
            break
    if not font_path:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    intro_bg = ColorClip(size=(W, H), color=(0, 0, 0), duration=duration)

    red_bar = ColorClip(size=(W, 8), color=(255, 0, 0), duration=duration).with_position((0, H // 2 - 60))
    blue_bar = ColorClip(size=(W, 8), color=(0, 50, 150), duration=duration).with_position((0, H // 2 + 50))

    channel_name = TextClip(
        text="FOOTBALL HIGHLIGHTS DAILY",
        font_size=60, color="white", font=font_path, text_align="center"
    ).with_position(("center", H // 2 - 40)).with_duration(duration)

    subtitle = TextClip(
        text="WORLD CUP 2026 - LIVE COVERAGE",
        font_size=32, color=(255, 215, 0), font=font_path, text_align="center"
    ).with_position(("center", H // 2 + 20)).with_duration(duration)

    year = TextClip(
        text="2026",
        font_size=120, color=(255, 255, 255), font=font_path, text_align="center"
    ).with_position(("center", H // 2 - 100)).with_duration(duration).with_opacity(0.15)

    news_flash = TextClip(
        text="BREAKING NEWS",
        font_size=28, color="white", font=font_path
    ).with_position(("center", H - 40)).with_duration(duration)

    ticker_bg = ColorClip(size=(W, 40), color=(255, 0, 0), duration=duration).with_position((0, H - 50))

    video = CompositeVideoClip([intro_bg, year, red_bar, blue_bar, channel_name, subtitle, ticker_bg, news_flash])

    video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac",
                          preset="ultrafast", threads=2, ffmpeg_params=["-crf", "23"])
    video.close()
    return output_path


def create_tv_outro(output_path, duration=3):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    font_path = None
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "arial.ttf", "Arial.ttf"]:
        if os.path.exists(f):
            font_path = f
            break
    if not font_path:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    outro_bg = ColorClip(size=(W, H), color=(0, 0, 0), duration=duration)

    thanks = TextClip(
        text="THANKS FOR WATCHING",
        font_size=60, color="white", font=font_path, text_align="center"
    ).with_position(("center", H // 2 - 80)).with_duration(duration)

    sub = TextClip(
        text="SUBSCRIBE FOR DAILY WORLD CUP UPDATES!",
        font_size=36, color=(255, 215, 0), font=font_path, text_align="center"
    ).with_position(("center", H // 2)).with_duration(duration)

    bell = TextClip(
        text="HIT THE BELL ICON!",
        font_size=28, color="white", font=font_path, text_align="center"
    ).with_position(("center", H // 2 + 60)).with_duration(duration)

    red = ColorClip(size=(W, 6), color=(255, 0, 0), duration=duration).with_position((0, H // 2 - 30))
    blue = ColorClip(size=(W, 6), color=(0, 50, 150), duration=duration).with_position((0, H // 2 + 110))

    video = CompositeVideoClip([outro_bg, red, blue, thanks, sub, bell])
    video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac",
                          preset="ultrafast", threads=2, ffmpeg_params=["-crf", "23"])
    video.close()
    return output_path


def create_watermark(output_path):
    size = 200
    img = Image.new("RGBA", (size, size // 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    font = _get_font(36)
    font_sm = _get_font(18)

    draw.rounded_rectangle([5, 5, size - 5, size // 2 - 5], radius=10, fill=(0, 50, 150, 200))

    bbox = draw.textbbox((0, 0), "FHD", font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((size - tw) // 2, 8), "FHD", fill=(255, 255, 255, 230), font=font)

    bbox2 = draw.textbbox((0, 0), "LIVE", font=font_sm)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((size - tw2) // 2, size // 2 - 28), "LIVE", fill=(255, 215, 0, 230), font=font_sm)

    img.save(output_path, "PNG")
    return output_path
