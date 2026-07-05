import os
import random
import math
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from moviepy.audio.fx import AudioFadeIn, AudioFadeOut
from src.config import Config
from src.trends_fetcher import get_trending_sports_topics


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


def _make_fifa_bg(theme_idx, frame=0):
    W, H = 1080, 1920
    palettes = [
        ((0, 20, 60), (0, 80, 180)),
        ((60, 0, 0), (180, 20, 20)),
        ((0, 40, 20), (0, 100, 60)),
        ((40, 0, 60), (100, 0, 120)),
    ]
    c1, c2 = palettes[theme_idx % len(palettes)]
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    for i in range(12):
        x = int(W * 0.05 + i * W * 0.08 + 15 * math.sin(frame * 0.04 + i * 2))
        y = int(H * 0.05 + i * H * 0.08 + 20 * math.cos(frame * 0.06 + i * 1.5))
        sz = 25 + 8 * math.sin(frame * 0.05 + i)
        draw.ellipse([x - sz, y - sz, x + sz, y + sz], fill=(255, 215, 0, 30))
    draw.rectangle([0, 0, W, 4], fill=(255, 215, 0))
    draw.rectangle([0, H - 4, W, H], fill=(255, 215, 0))
    return img


def _build_viral_facts():
    raw = get_trending_sports_topics()
    facts = []
    for topic in raw:
        facts.append({
            "title": f"Viral! {topic.title()} #shorts #football",
            "script": f"Did you know? {topic} This is going viral! Follow for more football updates!",
        })
    return facts


def generate_viral_shorts(output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(Config.OUTPUT_DIR, "shorts")
    os.makedirs(output_dir, exist_ok=True)
    facts = _build_viral_facts()
    results = []
    count = min(2, len(facts))
    for i in range(count):
        output_path = os.path.join(output_dir, f"fifa_short_{i+1}.mp4")
        try:
            W, H = 1080, 1920
            part_duration = 5
            frames = []
            for f in range(2):
                scene = _make_fifa_bg(i, f)
                draw = ImageDraw.Draw(scene)
                title = facts[i]["title"].replace("#shorts #football", "").strip()
                font_large = _get_font(64)
                font_medium = _get_font(42)
                words = title.split()
                lines = []
                current = ""
                for w in words:
                    test = current + " " + w if current else w
                    bbox = draw.textbbox((0, 0), test, font=font_large)
                    if bbox[2] - bbox[0] <= W - 120:
                        current = test
                    else:
                        if current:
                            lines.append(current)
                        current = w
                if current:
                    lines.append(current)
                y_start = H // 2 - len(lines) * 40
                for li, line in enumerate(lines):
                    bbox = draw.textbbox((0, 0), line, font=font_large)
                    x_pos = (W - (bbox[2] - bbox[0])) // 2
                    draw.text((x_pos + 3, y_start + li * 80 + 3), line, fill=(0, 0, 0), font=font_large)
                    draw.text((x_pos, y_start + li * 80), line, fill=(255, 255, 255), font=font_large)
                draw.text((W // 2 - 100, H - 120), "FOLLOW FOR MORE", fill=(255, 215, 0), font=font_medium)
                frame_path = output_path.replace(".mp4", f"_part{f}.png")
                scene.save(frame_path, quality=95)
                frames.append(frame_path)
            clips = []
            for fp in frames:
                clip = ImageClip(fp, duration=part_duration)
                clip = clip.with_effects([AudioFadeIn(0.3), AudioFadeOut(0.3)])
                clips.append(clip)
            video = concatenate_videoclips(clips, method="compose")
            voice_path = os.path.join(output_dir, f"short_{i+1}_voice.mp3")
            try:
                import edge_tts
                import asyncio
                text = facts[i]["script"]
                async def _run():
                    tts = edge_tts.Communicate(text, voice="en-US-GuyNeural", rate="-5%", pitch="0Hz")
                    await tts.save(voice_path)
                asyncio.run(_run())
                if os.path.getsize(voice_path) > 1000:
                    audio = AudioFileClip(voice_path)
                    video = video.with_audio(audio)
            except Exception:
                pass
            video.write_videofile(output_path, fps=24, codec="libx264", preset="fast", threads=4, logger=None)
            for fp in frames:
                if os.path.exists(fp):
                    os.remove(fp)
            if os.path.exists(voice_path):
                os.remove(voice_path)
            theme = facts[i]
            results.append({
                "path": output_path,
                "info": {
                    "title": theme["title"],
                    "script": theme["script"],
                    "duration": part_duration * 2,
                    "hashtags": ["shorts", "football", "viral", "soccer", "trending"],
                },
            })
            print(f"  FIFA Short {i+1}: {theme['title'][:50]}...")
        except Exception as e:
            print(f"  FIFA Short {i+1} failed: {e}")
    return results


if __name__ == "__main__":
    results = generate_viral_shorts()
    for r in results:
        print(f"\nFIFA Short: {r['info']['title']}")
