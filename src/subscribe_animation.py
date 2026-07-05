import os
import random
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip
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


def _make_subscribe_frame(w, h):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    stars = ["★", "✦", "✧", "☆"]
    for _ in range(40):
        x = random.randint(0, w)
        y = random.randint(0, h)
        c = random.choice(stars)
        s = random.randint(10, 28)
        a = random.randint(40, 120)
        draw.text((x, y), c, fill=(255, 215, 0, a), font=_get_font(s))

    cx, cy = w // 2, h // 2
    bw, bh = 340, 100

    for g in range(3, 0, -1):
        draw.rounded_rectangle(
            [(cx - bw // 2 - 6 * g, cy - bh // 2 - 6 * g),
             (cx + bw // 2 + 6 * g, cy + bh // 2 + 6 * g)],
            radius=28, fill=(255, 50, 50, 20 // max(g, 1)),
        )

    draw.rounded_rectangle(
        [(cx - bw // 2, cy - bh // 2), (cx + bw // 2, cy + bh // 2)],
        radius=25, fill=(255, 50, 50),
    )
    draw.rounded_rectangle(
        [(cx - bw // 2 + 4, cy - bh // 2 + 4), (cx + bw // 2 - 4, cy + bh // 2 - 4)],
        radius=22, fill=(220, 30, 30),
    )

    bx = cx - 90
    by = cy
    bs = 28
    draw.ellipse([bx - bs, by - bs + 6, bx + bs, by + bs + 6], fill=(255, 215, 0))
    draw.rectangle([bx - 4, by - bs + 6 - 8, bx + 4, by - bs + 6], fill=(255, 215, 0))
    bx2 = cx + 90
    draw.ellipse([bx2 - bs, by - bs + 6, bx2 + bs, by + bs + 6], fill=(255, 215, 0))
    draw.rectangle([bx2 - 4, by - bs + 6 - 8, bx2 + 4, by - bs + 6], fill=(255, 215, 0))

    ft = _get_font(48)
    st = "SUBSCRIBE"
    sb = draw.textbbox((0, 0), st, font=ft)
    draw.text((cx - (sb[2] - sb[0]) // 2, cy - 28), st, fill=(255, 255, 255), font=ft)

    fs = _get_font(20)
    sm = "🔔 New kids songs every day!"
    smb = draw.textbbox((0, 0), sm, font=fs)
    draw.text(((w - (smb[2] - smb[0])) // 2, cy + 60), sm, fill=(255, 255, 200), font=fs)

    fl = _get_font(22)
    lt = "♪ Cortana Kids Songs ♪"
    lb = draw.textbbox((0, 0), lt, font=fl)
    draw.text(((w - (lb[2] - lb[0])) // 2, h - 55), lt, fill=(100, 200, 255), font=fl)

    return img


def create_subscribe_clip(duration=3.0, output_size=(1280, 720)):
    w, h = output_size
    frame = _make_subscribe_frame(w, h)
    path = "_subscribe_frame.png"
    frame.save(path, quality=92)

    clip = ImageClip(path, duration=duration)
    clip = clip.with_effects([FadeIn(0.5), FadeOut(0.5)])

    return clip, path


def cleanup_subscribe(path):
    if os.path.exists(path):
        os.remove(path)
