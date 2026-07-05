import os
import random
import math
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx import FadeIn, FadeOut


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
    glow = 20 + 10 * math.sin(frame * 0.1)
    for g in range(5, 0, -1):
        alpha = 40 // g
        draw.ellipse(
            [cx - r - glow * g, cy - r - glow * g, cx + r + glow * g, cy + r + glow * g],
            fill=(0, 120 + 20 * g, 255, alpha),
        )
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 150, 255))
    draw.ellipse([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5], fill=(50, 180, 255))
    eye_y = cy - int(r * 0.2)
    for eye_x in [cx - int(r * 0.35), cx + int(r * 0.35)]:
        draw.ellipse([eye_x - 6, eye_y - 6, eye_x + 6, eye_y + 6], fill=(255, 255, 255))
        draw.ellipse([eye_x - 3, eye_y - 3, eye_x + 3, eye_y + 3], fill=(0, 50, 100))
    mouth_y = cy + int(r * 0.3)
    mouth_open = 3 + 2 * math.sin(frame * 0.2)
    draw.arc(
        [cx - int(r * 0.3), mouth_y - int(r * 0.1), cx + int(r * 0.3), mouth_y + int(mouth_open)],
        0, 180, fill=(255, 100, 100), width=3,
    )
    for dot_x in range(cx - r + 5, cx + r - 5, 15):
        dot_y = cy - r - int(glow * 0.5) + 5 * math.sin(frame * 0.15 + dot_x * 0.1)
        if abs(dot_y - cy) < r * 0.8:
            draw.ellipse([dot_x - 3, dot_y - 3, dot_x + 3, dot_y + 3], fill=(100, 200, 255, 150))
    return cx, cy + r + 10


def _draw_kid(draw, cx, cy, size, skin_color=(255, 200, 150), shirt_color=(100, 200, 255), frame=0):
    bounce = 5 * math.sin(frame * 0.15)
    head_r = int(size * 0.25)
    body_h = int(size * 0.35)
    leg_h = int(size * 0.3)
    arm_w = int(size * 0.08)
    total_h = head_r * 2 + body_h + leg_h
    top_y = cy - total_h // 2 + bounce
    head_y = top_y
    draw.ellipse([cx - head_r, head_y, cx + head_r, head_y + head_r * 2], fill=skin_color)
    hair_y = head_y - int(head_r * 0.3)
    hair_colors = [(255, 200, 50), (150, 80, 30), (50, 50, 50), (255, 150, 100)]
    hair_c = random.choice(hair_colors)
    draw.ellipse([cx - head_r - 3, hair_y, cx + head_r + 3, hair_y + head_r], fill=hair_c)
    eye_y2 = head_y + int(head_r * 0.5)
    for ex in [cx - int(head_r * 0.35), cx + int(head_r * 0.35)]:
        draw.ellipse([ex - 3, eye_y2 - 3, ex + 3, eye_y2 + 3], fill=(0, 0, 0))
        draw.ellipse([ex - 1, eye_y2 - 1, ex + 1, eye_y2 + 1], fill=(255, 255, 255))
    mouth_y2 = head_y + int(head_r * 1.2)
    draw.arc([cx - int(head_r * 0.3), mouth_y2 - 3, cx + int(head_r * 0.3), mouth_y2 + 3], 0, 180, fill=(200, 50, 50), width=2)
    body_top = head_y + head_r * 2
    draw.rounded_rectangle(
        [cx - body_h // 2, body_top, cx + body_h // 2, body_top + body_h],
        radius=8, fill=shirt_color,
    )
    leg_x = cx - int(body_h * 0.25)
    leg_swing = 5 * math.sin(frame * 0.2)
    draw.line([(leg_x, body_top + body_h), (leg_x - 5 + leg_swing, body_top + body_h + leg_h)], fill=(50, 50, 150), width=arm_w)
    leg_x2 = cx + int(body_h * 0.25)
    draw.line([(leg_x2, body_top + body_h), (leg_x2 + 5 - leg_swing, body_top + body_h + leg_h)], fill=(50, 50, 150), width=arm_w)
    arm_swing = 8 * math.sin(frame * 0.15)
    draw.line([(cx - body_h // 2, body_top + 10), (cx - body_h // 2 - 15 + arm_swing, body_top + body_h // 2)], fill=skin_color, width=arm_w)
    draw.line([(cx + body_h // 2, body_top + 10), (cx + body_h // 2 + 15 - arm_swing, body_top + body_h // 2)], fill=skin_color, width=arm_w)


def _draw_background(draw, W, H, theme="rainbow", frame=0):
    sky_colors = {
        "rainbow": [(100, 180, 255), (200, 230, 255), (50, 200, 100)],
        "bunny": [(180, 220, 255), (220, 240, 255), (100, 200, 100)],
        "stars": [(10, 10, 50), (20, 20, 80), (30, 30, 60)],
        "fish": [(0, 50, 100), (0, 100, 150), (0, 150, 200)],
        "train": [(200, 220, 255), (230, 240, 255), (100, 180, 100)],
        "cat": [(255, 200, 220), (255, 220, 240), (200, 150, 100)],
        "morning": [(255, 200, 100), (255, 220, 150), (100, 200, 100)],
    }
    colors = sky_colors.get(theme, sky_colors["rainbow"])
    for y in range(H):
        ratio = y / H
        r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * ratio)
        g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * ratio)
        b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    ground_y = int(H * 0.78)
    draw.rectangle([0, ground_y, W, H], fill=colors[2])
    draw.rectangle([0, ground_y - 5, W, ground_y], fill=(colors[2][0] + 30, colors[2][1] + 30, colors[2][2] + 30))
    if theme in ["stars", "morning"]:
        for _ in range(60):
            sx = random.randint(0, W)
            sy = random.randint(0, ground_y - 50)
            twinkle = 150 + 105 * math.sin(frame * 0.05 + sx * 0.01 + sy * 0.01)
            draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(int(twinkle), int(twinkle), int(twinkle * 0.8)))
    if theme == "rainbow":
        for i in range(7):
            colors_r = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]
            offset = int(20 * math.sin(frame * 0.05 + i))
            cx_r = W // 2 + offset
            cy_r = ground_y - 50
            draw.arc([cx_r - 300 - i * 20, cy_r - 250, cx_r + 300 + i * 20, cy_r + 50],
                     180, 360, fill=colors_r[i], width=12)
    if theme in ["fish"]:
        for _ in range(10 + int(5 * math.sin(frame * 0.03))):
            bx = random.randint(0, W)
            by = random.randint(100, ground_y - 50)
            draw.ellipse([bx - 10, by - 6, bx + 10, by + 6], fill=(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
            draw.polygon([(bx + 10, by), (bx + 18, by - 5), (bx + 18, by + 5)], fill=(200, 200, 200))
    if theme in ["train"]:
        for _ in range(3):
            tx = (frame * 2 + _ * 400) % (W + 200) - 100
            draw.rectangle([tx, ground_y - 40, tx + 80, ground_y - 5], fill=(255, 50, 50))
            draw.rectangle([tx + 10, ground_y - 55, tx + 30, ground_y - 40], fill=(50, 50, 50))
            draw.ellipse([tx + 10, ground_y - 5, tx + 25, ground_y + 10], fill=(50, 50, 50))
            draw.ellipse([tx + 55, ground_y - 5, tx + 70, ground_y + 10], fill=(50, 50, 50))
    if theme in ["cat", "bunny"]:
        for _ in range(6):
            fx = random.randint(100, W - 100)
            fy = random.randint(ground_y + 10, H - 20)
            fcolors = [(255, 100, 100), (255, 255, 100), (255, 150, 200), (200, 100, 255)]
            fc = random.choice(fcolors)
            for p in range(5):
                angle = math.radians(p * 72 - 90)
                px = fx + int(15 * math.cos(angle))
                py = fy + int(15 * math.sin(angle))
                draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=fc)
            draw.ellipse([fx - 3, fy - 3, fx + 3, fy + 3], fill=(255, 200, 50))


def _create_lyrics_frame(lyrics_group, line_index, total_groups, theme="rainbow", frame=0, W=1920, H=1080):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    _draw_background(draw, W, H, theme, frame)
    cortana_x = W // 2
    cortana_y = H // 4
    _draw_cortana(draw, cortana_x, cortana_y, 80, frame)
    kid_x = W // 2 - 200
    kid_y = H - 250
    shirt_colors = [(100, 200, 255), (255, 100, 100), (100, 255, 100), (255, 200, 50), (200, 100, 255)]
    _draw_kid(draw, kid_x, kid_y, 220, shirt_color=shirt_colors[line_index % len(shirt_colors)], frame=frame)
    kid2_x = W // 2 + 200
    _draw_kid(draw, kid2_x, kid_y + 10, 190, skin_color=(220, 180, 120), shirt_color=shirt_colors[(line_index + 2) % len(shirt_colors)], frame=frame + 10)
    for i in range(6):
        sx = 100 + i * 300 + int(50 * math.sin(frame * 0.08 + i))
        sy = H // 2 - 100 + int(30 * math.cos(frame * 0.1 + i * 1.5))
        sc = [(255, 215, 0), (255, 255, 200), (255, 200, 100)][i % 3]
        _draw_star_shape(draw, sx, sy, 10 + 5 * math.sin(frame * 0.12 + i), sc)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([W // 2 - 450, H - 190, W // 2 + 450, H - 20], fill=(0, 0, 0, 160))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    font_large = _get_font(48)
    font_small = _get_font(26)
    y_pos = H - 165
    for line in lyrics_group:
        if not line.strip():
            y_pos += 30
            continue
        bbox = draw.textbbox((0, 0), line, font=font_large)
        tw = bbox[2] - bbox[0]
        x_pos = (W - tw) // 2
        draw.text((x_pos + 2, y_pos + 2), line, fill=(0, 0, 0), font=font_large)
        draw.text((x_pos, y_pos), line, fill=(255, 255, 255), font=font_large)
        y_pos += 50
    progress = f"{line_index + 1}/{total_groups}"
    draw.text((W - 110, 20), progress, fill=(200, 200, 200), font=font_small)
    draw.text((20, 20), "SUBSCRIBE", fill=(255, 200, 50), font=font_small)
    draw.text((20, 45), "KIDS SONGS", fill=(255, 255, 255), font=font_small)
    return img


def _draw_star_shape(draw, cx, cy, size, fill):
    points = []
    for i in range(10):
        angle = math.radians(-90 + i * 36)
        r = size if i % 2 == 0 else size * 0.4
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill)


def create_kids_song_video(song_data, output_path, voice_path=None, W=1920, H=1080):
    lyrics = song_data["lyrics"]
    theme = song_data.get("theme", "rainbow")
    total_duration = 60
    if voice_path and os.path.exists(voice_path) and os.path.getsize(voice_path) > 1000:
        try:
            audio = AudioFileClip(voice_path)
            total_duration = max(audio.duration + 2, 30)
        except Exception:
            total_duration = 60
    line_groups = []
    group_size = max(1, len(lyrics) // max(1, int(total_duration // 7)))
    for i in range(0, len(lyrics), group_size):
        group = lyrics[i:i + group_size]
        if any(l.strip() for l in group):
            line_groups.append(group)
    group_duration = total_duration / len(line_groups)
    frames_per_group = max(1, int(group_duration * 3))
    clip_paths = []
    for gi, group in enumerate(line_groups):
        group_frames = []
        for f in range(frames_per_group):
            frame = _create_lyrics_frame(group, gi, len(line_groups), theme, f, W, H)
            frame_path = output_path.replace(".mp4", f"_g{gi}_f{f}.png")
            frame.save(frame_path, quality=92)
            group_frames.append(frame_path)
        seg_duration = len(group_frames) / 3
        clip = ImageClip(group_frames[0], duration=seg_duration)
        clip = clip.with_effects([FadeIn(0.2), FadeOut(0.2)])
        clip_paths.append(clip)
    video = concatenate_videoclips(clip_paths, method="compose")
    if voice_path and os.path.exists(voice_path) and os.path.getsize(voice_path) > 1000:
        try:
            audio = AudioFileClip(voice_path)
            video = video.with_audio(audio)
        except Exception:
            pass
    video.write_videofile(output_path, fps=24, codec="libx264", preset="fast", threads=4, logger=None)
    for gi in range(len(line_groups)):
        for f in range(frames_per_group if 'frames_per_group' in dir() else 0):
            p = output_path.replace(".mp4", f"_g{gi}_f{f}.png")
            if os.path.exists(p):
                os.remove(p)
    thumb_path = output_path.replace(".mp4", "_thumb.jpg")
    thumb = _create_lyrics_frame(line_groups[0] if line_groups else ["Kids Song"], 0, 1, theme, 0, W, H)
    thumb = thumb.resize((1280, 720), Image.LANCZOS)
    draw = ImageDraw.Draw(thumb)
    title = song_data.get("title", "Kids Song")
    font_large = _get_font(50)
    bbox = draw.textbbox((0, 0), title, font=font_large)
    tw = bbox[2] - bbox[0]
    draw.rectangle([(1280 - tw) // 2 - 20, 300, (1280 + tw) // 2 + 20, 370], fill=(0, 0, 0, 200))
    draw.text(((1280 - tw) // 2, 310), title, fill=(255, 255, 255), font=font_large)
    thumb.save(thumb_path, quality=90)
    return output_path, thumb_path
