import os
import random
import math
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
from moviepy.audio.fx import AudioFadeIn, AudioFadeOut, MultiplyVolume
from src.config import Config
from src.trends_fetcher import get_trending_kids_topics


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


def _draw_cortana(draw, cx, cy, size, frame=0):
    r = size
    glow = 15 + 8 * math.sin(frame * 0.1)
    for g in range(5, 0, -1):
        alpha = 30 // g
        draw.ellipse(
            [cx - r - glow * g, cy - r - glow * g, cx + r + glow * g, cy + r + glow * g],
            fill=(0, 120 + 20 * g, 255, alpha),
        )
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 150, 255))
    draw.ellipse([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5], fill=(50, 180, 255))
    eye_y = cy - int(r * 0.2)
    for eye_x in [cx - int(r * 0.35), cx + int(r * 0.35)]:
        draw.ellipse([eye_x - 5, eye_y - 5, eye_x + 5, eye_y + 5], fill=(255, 255, 255))
        draw.ellipse([eye_x - 2, eye_y - 2, eye_x + 2, eye_y + 2], fill=(0, 50, 100))
    mouth_y = cy + int(r * 0.3)
    draw.arc(
        [cx - int(r * 0.25), mouth_y - 2, cx + int(r * 0.25), mouth_y + 3],
        0, 180, fill=(255, 100, 100), width=2,
    )


def _draw_kid(draw, cx, cy, size, skin_color=(255, 200, 150), shirt_color=(100, 200, 255), frame=0):
    bounce = 3 * math.sin(frame * 0.15)
    head_r = int(size * 0.25)
    body_h = int(size * 0.35)
    leg_h = int(size * 0.3)
    total_h = head_r * 2 + body_h + leg_h
    top_y = cy - total_h // 2 + bounce
    head_y = top_y
    draw.ellipse([cx - head_r, head_y, cx + head_r, head_y + head_r * 2], fill=skin_color)
    hair_y = head_y - int(head_r * 0.3)
    hair_color = random.choice([(255, 200, 50), (150, 80, 30), (50, 50, 50), (255, 150, 100)])
    draw.ellipse([cx - head_r - 3, hair_y, cx + head_r + 3, hair_y + head_r], fill=hair_color)
    eye_y2 = head_y + int(head_r * 0.5)
    for ex in [cx - int(head_r * 0.35), cx + int(head_r * 0.35)]:
        draw.ellipse([ex - 3, eye_y2 - 3, ex + 3, eye_y2 + 3], fill=(0, 0, 0))
        draw.ellipse([ex - 1, eye_y2 - 1, ex + 1, eye_y2 + 1], fill=(255, 255, 255))
    mouth_y2 = head_y + int(head_r * 1.2)
    draw.arc([cx - int(head_r * 0.3), mouth_y2 - 2, cx + int(head_r * 0.3), mouth_y2 + 2], 0, 180, fill=(200, 50, 50), width=2)
    body_top = head_y + head_r * 2
    draw.rounded_rectangle(
        [cx - body_h // 2, body_top, cx + body_h // 2, body_top + body_h],
        radius=6, fill=shirt_color,
    )
    leg_swing = 3 * math.sin(frame * 0.2)
    for lx in [cx - int(body_h * 0.25), cx + int(body_h * 0.25)]:
        lx2 = lx + leg_swing if lx < cx else lx - leg_swing
        draw.line([(lx, body_top + body_h), (lx2, body_top + body_h + leg_h)], fill=(50, 50, 150), width=6)
    arm_swing = 5 * math.sin(frame * 0.15)
    draw.line([(cx - body_h // 2, body_top + 8), (cx - body_h // 2 - 10 + arm_swing, body_top + body_h // 2)], fill=skin_color, width=6)
    draw.line([(cx + body_h // 2, body_top + 8), (cx + body_h // 2 + 10 - arm_swing, body_top + body_h // 2)], fill=skin_color, width=6)


def _create_cortana_scene(theme_idx, frame=0):
    W, H = 1080, 1920
    palettes = [
        {"sky": [(100, 180, 255), (200, 230, 255)], "ground": (50, 200, 100)},
        {"sky": [(255, 150, 100), (255, 200, 150)], "ground": (150, 100, 200)},
        {"sky": [(180, 100, 255), (220, 180, 255)], "ground": (50, 200, 150)},
        {"sky": [(50, 200, 200), (150, 230, 230)], "ground": (100, 220, 100)},
    ]
    pal = palettes[theme_idx % len(palettes)]
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        r = int(pal["sky"][0][0] + (pal["sky"][1][0] - pal["sky"][0][0]) * ratio)
        g = int(pal["sky"][0][1] + (pal["sky"][1][1] - pal["sky"][0][1]) * ratio)
        b = int(pal["sky"][0][2] + (pal["sky"][1][2] - pal["sky"][0][2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    ground_y = int(H * 0.75)
    draw.rectangle([0, ground_y, W, H], fill=pal["ground"])
    draw.rectangle([0, ground_y - 5, W, ground_y], fill=(pal["ground"][0] + 30, pal["ground"][1] + 30, pal["ground"][2] + 30))
    _draw_cortana(draw, W // 2, H // 3, 100, frame)
    kid1_x = W // 2 - 180
    kid1_y = H - 300
    _draw_kid(draw, kid1_x, kid1_y, 200, shirt_color=(100, 200, 255), frame=frame)
    kid2_x = W // 2 + 180
    _draw_kid(draw, kid2_x, kid1_y + 10, 170, skin_color=(220, 180, 120), shirt_color=(255, 100, 100), frame=frame + 8)
    for i in range(5):
        sx = 150 + i * 200
        sy = 150 + int(50 * math.sin(frame * 0.05 + i * 2))
        draw.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=(255, 215, 0))
    return img


def _build_kids_facts():
    raw = get_trending_kids_topics()
    facts = []
    for topic in raw:
        facts.append({
            "title": f"Did You Know? {topic.title()}! #shorts #kids",
            "script": f"Did you know? {topic}. Subscribe for more fun facts with Cortana!",
        })
    return facts


def generate_viral_shorts(output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(Config.OUTPUT_DIR, "shorts")
    os.makedirs(output_dir, exist_ok=True)
    facts = _build_kids_facts()
    results = []
    count = min(2, len(facts))
    for i in range(count):
        output_path = os.path.join(output_dir, f"kids_short_{i+1}.mp4")
        try:
            W, H = 1080, 1920
            part_duration = 5
            frames = []
            for f in range(2):
                scene = _create_cortana_scene(i, f)
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
            text = facts[i]["script"]
            try:
                import edge_tts
                import asyncio
                async def _run():
                    tts = edge_tts.Communicate(text, voice="en-US-JennyNeural", rate="+15%")
                    await tts.save(voice_path)
                asyncio.run(_run())
            except Exception as e:
                print(f"  edge-tts failed: {e}")
            if not os.path.exists(voice_path) or os.path.getsize(voice_path) < 1000:
                try:
                    from gtts import gTTS
                    tts = gTTS(text=text, lang="en", slow=False, tld="com")
                    tts.save(voice_path)
                except Exception as e2:
                    print(f"  gTTS failed: {e2}")
            audio_clips = []
            if os.path.exists(voice_path) and os.path.getsize(voice_path) > 1000:
                try:
                    audio_clips.append(AudioFileClip(voice_path))
                except Exception as e:
                    print(f"  Voice load failed: {e}")
            try:
                from src.music_generator import generate_kids_background
                music_path = generate_kids_background(part_duration * 2)
                if os.path.exists(music_path):
                    bg_music = AudioFileClip(music_path).with_effects([MultiplyVolume(0.25)])
                    audio_clips.append(bg_music)
            except Exception as e:
                print(f"  Music gen failed: {e}")
            if audio_clips:
                try:
                    final_audio = CompositeAudioClip(audio_clips)
                    video = video.with_audio(final_audio)
                except Exception as e:
                    print(f"  Audio mix failed: {e}")
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
                    "hashtags": ["shorts", "kids", "funfacts", "learning", "cortana"],
                },
            })
            print(f"  Kids Short {i+1}: {theme['title'][:50]}...")
        except Exception as e:
            print(f"  Kids Short {i+1} failed: {e}")
    return results


if __name__ == "__main__":
    results = generate_viral_shorts()
    for r in results:
        print(f"\nKids Short: {r['info']['title']}")
