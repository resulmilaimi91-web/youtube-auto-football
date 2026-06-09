import os
import random
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    ImageClip, AudioFileClip, concatenate_videoclips, afx
)
from src.config import Config


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


VIRAL_SHORTS = [
    {
        "title": "World Cup 2026 Will BREAK The Internet! #shorts #worldcup2026 #viral",
        "script": "World Cup 2026 will be the biggest event in human history. 48 teams. 16 cities. 104 matches. 39 days of non-stop football. 82 thousand fans in the final. 5 billion viewers worldwide. This is not just a tournament. This is a revolution. Are you ready for the greatest World Cup ever?",
        "bg": [(255, 0, 0), (200, 0, 0)],
        "text": (255, 255, 255),
        "accent": (255, 215, 0),
        "hooks": ["STOP SCROLLING!", "THIS WILL BLOW YOUR MIND!", "YOU ARE NOT READY!"],
    },
    {
        "title": "Football Players Are NOT Human! #shorts #football #insane #viral",
        "script": "These football players are not human. The speed. The power. The technique. They defy physics. They break the laws of nature. They do things we thought were impossible. This is why football is the beautiful game. This is why we watch. This is why we love it.",
        "bg": [(0, 0, 0), (30, 0, 60)],
        "text": (255, 255, 255),
        "accent": (0, 255, 0),
        "hooks": ["WATCH THIS!", "THIS IS INSANE!", "NO WAY!"],
    },
]


def _create_viral_frame(W, H, theme, hook_text, part=0):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    c1, c2 = theme["bg"]

    for y in range(H):
        ratio = y / H
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    for i in range(60):
        x = random.randint(0, W)
        y = random.randint(0, H)
        size = random.randint(1, 4)
        brightness = random.randint(150, 255)
        draw.ellipse([x - size, y - size, x + size, y + size], fill=(brightness, brightness, brightness))

    font_hook = _get_font(100)
    font_big = _get_font(72)
    font_med = _get_font(48)

    hook_y = 200
    bbox = draw.textbbox((0, 0), hook_text, font=font_hook)
    tw = bbox[2] - bbox[0]
    draw.text((W // 2 - tw // 2 + 5, hook_y + 5), hook_text, fill=(0, 0, 0), font=font_hook)
    draw.text((W // 2 - tw // 2, hook_y), hook_text, fill=theme["accent"], font=font_hook)

    if part == 0:
        cx, cy = W // 2, H // 2
        draw.ellipse([cx - 150, cy - 150, cx + 150, cy + 150], fill=(255, 255, 255))
        draw.polygon([(cx - 50, cy - 80), (cx - 50, cy + 80), (cx + 80, cy)], fill=theme["accent"])

        draw.rectangle([80, H - 400, W - 80, H - 280], fill=(0, 0, 0))
        draw.rectangle([80, H - 400, W - 80, H - 280], outline=theme["accent"], width=4)
        draw.text((W // 2 - 250, H - 380), "SUBSCRIBE NOW!", fill=theme["accent"], font=font_big)
    elif part == 1:
        numbers = ["48", "104", "39", "82K"]
        labels = ["TEAMS", "MATCHES", "DAYS", "FANS"]
        for i, (num, label) in enumerate(zip(numbers, labels)):
            x = 135 + i * 270
            draw.ellipse([x - 80, H // 2 - 80, x + 80, H // 2 + 80], fill=(0, 0, 0))
            draw.ellipse([x - 75, H // 2 - 75, x + 75, H // 75 + 75], outline=theme["accent"], width=3)
            bbox_n = draw.textbbox((0, 0), num, font=font_big)
            tw_n = bbox_n[2] - bbox_n[0]
            draw.text((x - tw_n // 2, H // 2 - 40), num, fill=theme["accent"], font=font_big)
            bbox_l = draw.textbbox((0, 0), label, font=font_med)
            tw_l = bbox_l[2] - bbox_l[0]
            draw.text((x - tw_l // 2, H // 2 + 50), label, fill=theme["text"], font=font_med)

        draw.rectangle([80, H - 300, W - 80, H - 200], fill=(255, 0, 0))
        draw.text((W // 2 - 200, H - 285), "LIKE & SHARE!", fill=(255, 255, 255), font=font_big)

    draw.rectangle([0, 0, W, 8], fill=theme["accent"])
    draw.rectangle([0, H - 8, W, H], fill=theme["accent"])

    return img


def create_viral_short(theme_idx, output_path, voice_path=None):
    theme = VIRAL_SHORTS[theme_idx % len(VIRAL_SHORTS)]
    W, H = 1080, 1920
    part_duration = 4

    frames = []
    for part in range(2):
        hook = theme["hooks"][part % len(theme["hooks"])]
        frame = _create_viral_frame(W, H, theme, hook, part)
        frame_path = output_path.replace(".mp4", f"_part{part}.png")
        frame.save(frame_path, quality=95)
        frames.append(frame_path)

    clips = []
    for i, frame_path in enumerate(frames):
        clip = ImageClip(frame_path, duration=part_duration)
        clip = clip.with_effects([afx.FadeIn(0.3), afx.FadeOut(0.3)])
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")

    if voice_path and os.path.exists(voice_path) and os.path.getsize(voice_path) > 1000:
        audio = AudioFileClip(voice_path)
        video = video.with_audio(audio)

    video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        preset="fast",
        threads=4,
        logger=None,
    )

    for fp in frames:
        if os.path.exists(fp):
            os.remove(fp)

    return output_path, {
        "title": theme["title"],
        "script": theme["script"],
        "duration": part_duration * 2,
        "hashtags": ["shorts", "football", "worldcup2026", "viral", "fifa"],
    }


def generate_viral_shorts(output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(Config.OUTPUT_DIR, "shorts")
    os.makedirs(output_dir, exist_ok=True)

    results = []
    for i in range(2):
        output_path = os.path.join(output_dir, f"viral_short_{i+1}.mp4")
        try:
            path, info = create_viral_short(i, output_path)
            results.append({"path": path, "info": info})
            print(f"  Viral Short {i+1}: {info['title'][:50]}...")
        except Exception as e:
            print(f"  Viral Short {i+1} failed: {e}")

    return results


if __name__ == "__main__":
    results = generate_viral_shorts()
    for r in results:
        print(f"\nViral Short: {r['info']['title']}")
        print(f"  Duration: {r['info']['duration']}s")
        print(f"  Path: {r['path']}")
