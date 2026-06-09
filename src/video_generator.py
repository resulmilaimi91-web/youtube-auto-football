import os
import textwrap
import random
import traceback
import sys
import urllib.request

from moviepy import (
    VideoFileClip, ColorClip, TextClip, AudioFileClip,
    CompositeVideoClip, CompositeAudioClip, afx, ImageClip,
    concatenate_videoclips
)
from PIL import Image, ImageDraw, ImageFont
from src.config import Config
from src.tv_assets import create_tv_intro, create_tv_outro, create_watermark, create_logo


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


def generate_voiceover(script_text, output_path):
    try:
        import edge_tts
        import asyncio
        voices = ["en-US-GuyNeural", "en-US-JennyNeural", "en-GB-RyanNeural", "en-US-TonyNeural", "en-AU-WilliamNeural"]
        voice = random.choice(voices)
        async def _run():
            tts = edge_tts.Communicate(script_text, voice=voice, rate="-2%", pitch="+0Hz", volume="+25%")
            await tts.save(output_path)
        asyncio.run(_run())
        if os.path.getsize(output_path) > 1000:
            return
    except Exception as e:
        print(f"edge-tts failed: {e}")

    try:
        from gtts import gTTS
        tts = gTTS(text=script_text, lang="en", slow=False, tld="com")
        tts.save(output_path)
        if os.path.getsize(output_path) > 1000:
            return
    except Exception as e2:
        print(f"gTTS failed: {e2}")
        with open(output_path, "wb") as f:
            f.write(b"")


def _download_image(url, path):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=10).read()
        if len(data) > 5000:
            with open(path, "wb") as f:
                f.write(data)
            return True
    except Exception:
        pass
    return False


def _make_zoom_clip(img_path, duration, W, H, zoom_type="in"):
    clip = ImageClip(img_path, duration=duration).resized((W, H))
    if zoom_type == "in":
        def zoom_in(get_frame, t):
            frame = get_frame(t)
            pil = Image.fromarray(frame)
            ratio = 1.0 + 0.15 * (t / duration)
            new_w = int(W * ratio)
            new_h = int(H * ratio)
            pil = pil.resize((new_w, new_h), Image.LANCZOS)
            left = (new_w - W) // 2
            top = (new_h - H) // 2
            pil = pil.crop((left, top, left + W, top + H))
            return list(pil.getdata())
        clip = clip.transform(zoom_in)
    elif zoom_type == "out":
        def zoom_out(get_frame, t):
            frame = get_frame(t)
            pil = Image.fromarray(frame)
            ratio = 1.15 - 0.15 * (t / duration)
            new_w = int(W * ratio)
            new_h = int(H * ratio)
            pil = pil.resize((new_w, new_h), Image.LANCZOS)
            left = (new_w - W) // 2
            top = (new_h - H) // 2
            pil = pil.crop((left, top, left + W, top + H))
            return list(pil.getdata())
        clip = clip.transform(zoom_out)
    return clip


def _make_split_screen(img_paths, duration, W, H):
    half_w = W // 2
    seg_dur = duration / max(len(img_paths), 1)
    clips = []
    for i in range(0, len(img_paths) - 1, 2):
        try:
            left = ImageClip(img_paths[i], duration=seg_dur).resized((half_w, H))
            right = ImageClip(img_paths[i + 1], duration=seg_dur).resized((half_w, H))
            right = right.with_position((half_w, 0))
            split = CompositeVideoClip([left, right], size=(W, H))
            clips.append(split)
        except Exception:
            pass
    if not clips:
        return None
    try:
        return concatenate_videoclips(clips, method="compose")
    except Exception:
        return clips[0]


def _get_topic_images(title):
    title_lower = title.lower()
    if any(w in title_lower for w in ["stadium", "venue", "host city", "cities"]):
        return [
            "football+stadium+night+lights",
            "soccer+stadium+panoramic+aerial",
            "world+cup+stadium+crowd+packed",
            "modern+football+stadium+architecture",
            "soccer+pitch+green+grass+perfect",
            "football+stadium+night+match+atmosphere",
            "soccer+stadium+fans+flags+colors",
            "football+arena+scoreboard+view",
        ]
    elif any(w in title_lower for w in ["player", "mbappe", "haaland", "bellingham", "star", "top 10", "best"]):
        return [
            "soccer+player+kicking+ball+action",
            "football+striker+goal+celebration",
            "soccer+player+skills+dribbling",
            "football+star+portrait+focus",
            "soccer+forward+shooting+power",
            "football+player+running+speed",
            "soccer+midfielder+passing+technique",
            "football+goalkeeper+save+dive",
        ]
    elif any(w in title_lower for w in ["trophy", "winner", "champion", "final", "lift"]):
        return [
            "world+cup+trophy+gold+shiny",
            "soccer+champion+celebration+trophy",
            "football+winner+medals+podium",
            "world+cup+final+celebration+confetti",
            "soccer+team+lifting+trophy",
            "football+champions+banner+flag",
            "world+cup+final+stadium+atmosphere",
            "soccer+gold+trophy+close+up",
        ]
    elif any(w in title_lower for w in ["goal", "score", "highlight", "save"]):
        return [
            "soccer+goal+net+ball+inside",
            "football+striker+scoring+goal",
            "soccer+goalkeeper+diving+save",
            "football+ball+hitting+crossbar",
            "soccer+free+kick+goal+spectacular",
            "football+ celebration+after+goal",
            "soccer+goal+replay+angle",
            "football+net+ball+close+up",
        ]
    elif any(w in title_lower for w in ["fan", "crowd", "support", "atmosphere"]):
        return [
            "football+fans+celebration+stadium",
            "soccer+crowd+flags+colors+banner",
            "world+cup+fans+party+atmosphere",
            "football+supporters+chanting+singing",
            "soccer+fans+face+paint+jersey",
            "football+stadium+crowd+wave",
            "soccer+fans+fireworks+celebration",
            "football+terrace+support+passion",
        ]
    elif any(w in title_lower for w in ["format", "team", "qualif", "group", "bracket"]):
        return [
            "world+cup+bracket+draw+poster",
            "soccer+teams+lineup+formation",
            "football+group+stage+table",
            "world+cup+qualification+map",
            "soccer+national+teams+flags",
            "football+draw+ceremony+stage",
            "world+cup+format+infographic",
            "soccer+match+schedule+calendar",
        ]
    else:
        return [
            "football+stadium+night+lights",
            "soccer+players+action+match",
            "world+cup+trophy+gold+championship",
            "football+fans+celebration+stadium",
            "soccer+goal+net+ball+score",
            "football+field+green+pitch",
            "soccer+boots+ball+grass",
            "football+champions+league+night",
        ]


def download_football_images(count=8, title=""):
    paths = []
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

    queries = _get_topic_images(title) if title else [
        "football+stadium+night+lights",
        "soccer+players+action+match",
        "world+cup+trophy+gold+championship",
        "football+fans+celebration+stadium",
        "soccer+goal+net+ball+score",
        "football+field+green+pitch",
        "soccer+boots+ball+grass",
        "football+champions+league+night",
    ]

    sources = [
        "https://source.unsplash.com/1920x1080/?{q}&sig={s}",
        "https://picsum.photos/1920/1080?random={s}",
        "https://loremflickr.com/1920/1080/{q}",
    ]

    used = set()
    for i in range(min(count * 2, len(queries))):
        if len(paths) >= count:
            break
        q = queries[i % len(queries)]
        sig = random.randint(1, 999999)
        path = os.path.join(Config.OUTPUT_DIR, f"scene_{len(paths)}.jpg")

        ok = False
        for src in sources:
            url = src.format(q=q, s=sig)
            ok = _download_image(url, path)
            if ok:
                fsize = os.path.getsize(path)
                if fsize > 10000:
                    paths.append(path)
                    break
                else:
                    os.remove(path)
                    ok = False

    return paths


def _make_gradient_bg(W, H, style=0):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    colors = [
        ((10, 15, 35), (20, 40, 80)),
        ((25, 10, 10), (60, 15, 15)),
        ((10, 25, 10), (15, 60, 15)),
        ((20, 15, 30), (40, 20, 60)),
        ((15, 20, 30), (30, 45, 70)),
        ((0, 30, 60), (0, 60, 120)),
    ]
    c1, c2 = colors[style % len(colors)]
    for y in range(H):
        r = int(c1[0] + (c2[0] - c1[0]) * y / H)
        g = int(c1[1] + (c2[1] - c1[1]) * y / H)
        b = int(c1[2] + (c2[2] - c1[2]) * y / H)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    return img


STYLES = ["classic", "breaking", "sports", "worldcup", "analysis", "news", "premium"]


def create_thumbnail(title, output_path, style=None):
    W, H = 1280, 720
    if style is None:
        style = random.choice(STYLES)

    style_idx = STYLES.index(style) if style in STYLES else 0
    bg = _make_gradient_bg(W, H, style_idx)
    draw = ImageDraw.Draw(bg)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    if style == "breaking":
        od.rectangle([0, 0, W, 90], fill=(255, 0, 0, 240))
        od.rectangle([0, H - 70, W, H], fill=(0, 0, 0, 200))
    elif style == "sports":
        od.rectangle([0, H - 100, W, H], fill=(0, 0, 0, 200))
        od.rectangle([0, 0, 10, H], fill=(255, 200, 0, 200))
    elif style == "worldcup":
        od.rectangle([0, 0, W, 80], fill=(0, 50, 120, 230))
        od.rectangle([0, H - 80, W, H], fill=(0, 50, 120, 230))
    elif style == "analysis":
        od.rectangle([0, 0, W, 60], fill=(20, 20, 20, 220))
        od.rectangle([0, H - 50, W, H], fill=(20, 20, 20, 220))
    elif style == "news":
        od.rectangle([0, 0, W, 100], fill=(200, 30, 30, 240))
        od.rectangle([0, H - 60, W, H], fill=(0, 0, 0, 220))
    elif style == "premium":
        od.rectangle([0, 0, W, 70], fill=(30, 30, 30, 220))
        od.rectangle([0, H - 70, W, H], fill=(30, 30, 30, 220))
        for i in range(3):
            od.line([(0, 70 + i), (W, 70 + i)], fill=(255, 215, 0, 150))
            od.line([(0, H - 73 + i), (W, H - 73 + i)], fill=(255, 215, 0, 150))
    else:
        od.rectangle([0, 380, W, H], fill=(0, 0, 0, 180))

    bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(bg)

    font = _get_font(54)
    small_font = _get_font(26)
    logo_font = _get_font(20)

    lines = textwrap.wrap(title, width=18)
    y = 140
    for line in lines[:3]:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (W - tw) // 2
        draw.text((x + 2, y + 2), line, fill=(0, 0, 0), font=font)
        draw.text((x, y), line, fill=(255, 255, 255), font=font)
        y += 68

    if style == "breaking":
        draw.rectangle([0, 0, W, 90], fill=(255, 0, 0))
        draw.text((W // 2 - 120, 28), "BREAKING NEWS", fill=(255, 255, 255), font=_get_font(38))
        draw.rectangle([0, H - 70, W, H], fill=(0, 0, 0))
        draw.text((W // 2 - 100, H - 50), "SUBSCRIBE NOW", fill=(255, 255, 255), font=small_font)
    elif style == "worldcup":
        draw.rectangle([0, 0, W, 80], fill=(0, 50, 120))
        draw.text((W // 2 - 140, 20), "FIFA WORLD CUP 2026", fill=(255, 215, 0), font=_get_font(34))
        draw.rectangle([0, H - 80, W, H], fill=(0, 50, 120))
        draw.text((W // 2 - 80, H - 55), "SUBSCRIBE NOW", fill=(255, 255, 255), font=small_font)
    elif style == "news":
        draw.rectangle([0, 0, W, 100], fill=(200, 30, 30))
        draw.text((40, 30), "LIVE", fill=(255, 255, 255), font=_get_font(40))
        draw.text((W // 2 - 100, 35), "FOOTBALL NEWS", fill=(255, 255, 255), font=_get_font(32))
        draw.rectangle([0, H - 60, W, H], fill=(0, 0, 0))
        draw.text((W // 2 - 80, H - 45), "SUBSCRIBE NOW", fill=(255, 255, 255), font=small_font)
    elif style == "premium":
        draw.rectangle([0, 0, W, 70], fill=(30, 30, 30))
        draw.text((40, 18), "FHD", fill=(255, 215, 0), font=_get_font(30))
        draw.text((100, 22), "PREMIUM", fill=(255, 255, 255), font=small_font)
        draw.rectangle([0, H - 70, W, H], fill=(30, 30, 30))
        draw.text((W // 2 - 80, H - 50), "SUBSCRIBE NOW", fill=(255, 255, 255), font=small_font)
    else:
        badge = Image.new("RGBA", (240, 50), (255, 0, 0, 255))
        bg.paste(badge, (W // 2 - 120, H - 90), badge)
        b_draw = ImageDraw.Draw(bg)
        b_draw.text((W // 2 - 85, H - 82), "SUBSCRIBE", fill=(255, 255, 255), font=small_font)

    logo_path = os.path.join(Config.OUTPUT_DIR, "logo.png")
    if not os.path.exists(logo_path):
        create_logo(logo_path)
    try:
        logo = Image.open(logo_path).resize((60, 60))
        bg.paste(logo, (W - 80, 10), logo)
    except Exception:
        pass

    draw2 = ImageDraw.Draw(bg)
    draw2.text((W - 180, 80), "FHD", fill=(255, 255, 255, 150), font=logo_font)

    bg.save(output_path, quality=92)
    return output_path


def create_video(script_data, output_path, style=None):
    VOICE_PATH = os.path.join(Config.OUTPUT_DIR, "voiceover.mp3")
    THUMB_PATH = os.path.join(Config.OUTPUT_DIR, "thumbnail.jpg")
    INTRO_PATH = os.path.join(Config.OUTPUT_DIR, "intro.mp4")
    OUTRO_PATH = os.path.join(Config.OUTPUT_DIR, "outro.mp4")
    WATERMARK_PATH = os.path.join(Config.OUTPUT_DIR, "watermark.png")
    BG_PATH = os.path.join(Config.ASSETS_DIR, "background.mp4")
    MUSIC_PATH = os.path.join(Config.ASSETS_DIR, "music.mp3")

    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

    generate_voiceover(script_data["script"], VOICE_PATH)

    if style is None:
        style = random.choice(STYLES)
    create_thumbnail(script_data["title"], THUMB_PATH, style)

    audio = AudioFileClip(VOICE_PATH)
    main_duration = audio.duration + 3

    W, H = Config.VIDEO_WIDTH, Config.VIDEO_HEIGHT

    print("  Generating intro...")
    intro_clip = VideoFileClip(create_tv_intro(INTRO_PATH, duration=4))

    print("  Generating outro...")
    outro_clip = VideoFileClip(create_tv_outro(OUTRO_PATH, duration=3))

    print("  Downloading topic images...")
    img_paths = download_football_images(8, script_data["title"])
    scenes = []
    if img_paths:
        seg_dur = main_duration / len(img_paths)
        for i, p in enumerate(img_paths):
            try:
                zoom = "in" if i % 2 == 0 else "out"
                clip = _make_zoom_clip(p, seg_dur, W, H, zoom)
                fade = min(0.5, seg_dur * 0.15)
                clip = clip.with_effects([afx.FadeIn(fade), afx.FadeOut(fade)])
                scenes.append(clip)
            except Exception:
                pass

    split_clip = _make_split_screen(img_paths[:4], min(6, main_duration * 0.3), W, H)
    if split_clip:
        try:
            scenes.insert(min(3, len(scenes)), split_clip)
        except Exception:
            pass

    if not scenes:
        bg_clip = ColorClip(size=(W, H), color=(10, 15, 30), duration=main_duration)
        scenes = [bg_clip]

    try:
        main_video = concatenate_videoclips(scenes, method="compose")
    except Exception:
        main_video = scenes[0].with_duration(main_duration)

    font_path = None
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "arial.ttf", "Arial.ttf"]:
        if os.path.exists(f):
            font_path = f
            break
    if not font_path and sys.platform == "linux":
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    overlays = []

    if style == "breaking":
        top = ColorClip(size=(W, 70), color=(255, 0, 0), duration=main_duration).with_position((0, 0))
        top_text = TextClip(text="BREAKING NEWS", font_size=32, color="white", font=font_path).with_position(("center", 18)).with_duration(main_duration)
        bottom = ColorClip(size=(W, 50), color=(0, 0, 0), duration=main_duration).with_position((0, H - 50))
        bottom_text = TextClip(text="SUBSCRIBE FOR MORE NEWS", font_size=22, color="white", font=font_path).with_position(("center", H - 40)).with_duration(main_duration)
        overlays.extend([top, top_text, bottom, bottom_text])
    elif style == "worldcup":
        top = ColorClip(size=(W, 70), color=(0, 50, 120), duration=main_duration).with_position((0, 0))
        top_text = TextClip(text="FIFA WORLD CUP 2026", font_size=30, color=(255, 215, 0), font=font_path).with_position(("center", 18)).with_duration(main_duration)
        bottom = ColorClip(size=(W, 50), color=(0, 50, 120), duration=main_duration).with_position((0, H - 50))
        bottom_text = TextClip(text="SUBSCRIBE NOW", font_size=22, color="white", font=font_path).with_position(("center", H - 40)).with_duration(main_duration)
        overlays.extend([top, top_text, bottom, bottom_text])
    elif style == "sports":
        side = ColorClip(size=(8, H), color=(255, 200, 0), duration=main_duration).with_position((0, 0))
        bottom = ColorClip(size=(W, 50), color=(0, 0, 0), duration=main_duration).with_position((0, H - 50))
        bottom_text = TextClip(text="FOOTBALL HIGHLIGHTS DAILY", font_size=22, color="white", font=font_path).with_position(("center", H - 40)).with_duration(main_duration)
        overlays.extend([side, bottom, bottom_text])
    elif style == "analysis":
        top = ColorClip(size=(W, 50), color=(20, 20, 20), duration=main_duration).with_position((0, 0))
        top_text = TextClip(text="TACTICAL ANALYSIS", font_size=26, color=(255, 200, 0), font=font_path).with_position((30, 10)).with_duration(main_duration)
        bottom = ColorClip(size=(W, 40), color=(20, 20, 20), duration=main_duration).with_position((0, H - 40))
        overlays.extend([top, top_text, bottom])
    elif style == "news":
        top = ColorClip(size=(W, 80), color=(200, 30, 30), duration=main_duration).with_position((0, 0))
        top_text = TextClip(text="LIVE", font_size=30, color="white", font=font_path).with_position((40, 22)).with_duration(main_duration)
        top_text2 = TextClip(text="FOOTBALL NEWS", font_size=28, color="white", font=font_path).with_position(("center", 22)).with_duration(main_duration)
        bottom = ColorClip(size=(W, 50), color=(0, 0, 0), duration=main_duration).with_position((0, H - 50))
        bottom_text = TextClip(text="SUBSCRIBE FOR DAILY UPDATES", font_size=22, color="white", font=font_path).with_position(("center", H - 40)).with_duration(main_duration)
        overlays.extend([top, top_text, top_text2, bottom, bottom_text])
    elif style == "premium":
        top = ColorClip(size=(W, 60), color=(30, 30, 30), duration=main_duration).with_position((0, 0))
        top_text = TextClip(text="FHD PREMIUM", font_size=26, color=(255, 215, 0), font=font_path).with_position((40, 15)).with_duration(main_duration)
        bottom = ColorClip(size=(W, 50), color=(30, 30, 30), duration=main_duration).with_position((0, H - 50))
        bottom_text = TextClip(text="SUBSCRIBE NOW", font_size=22, color="white", font=font_path).with_position(("center", H - 40)).with_duration(main_duration)
        gold_line1 = ColorClip(size=(W, 2), color=(255, 215, 0), duration=main_duration).with_position((0, 60))
        gold_line2 = ColorClip(size=(W, 2), color=(255, 215, 0), duration=main_duration).with_position((0, H - 52))
        overlays.extend([top, top_text, bottom, bottom_text, gold_line1, gold_line2])
    else:
        ticker = ColorClip(size=(W, 40), color=(255, 0, 0), duration=main_duration).with_position((0, H - 40))
        ticker_text = TextClip(text="FOOTBALL HIGHLIGHTS DAILY - SUBSCRIBE!", font_size=20, color="white", font=font_path).with_position(("center", H - 32)).with_duration(main_duration)
        overlays.extend([ticker, ticker_text])

    title_shadow = TextClip(
        text=script_data["title"], font_size=Config.TITLE_FONT_SIZE,
        color=(0, 0, 0), font=font_path, text_align="center",
        size=(W - 200, None), method="caption",
    ).with_position(("center", int(H * 0.35) + 3)).with_duration(main_duration).with_opacity(0.5)

    def slide_in_left(clip, delay=0):
        def pos(t):
            if t < delay:
                return (-clip.w, int(H * 0.35))
            progress = min(1.0, (t - delay) / 0.8)
            x = int(-clip.w + (W // 2 - clip.w // 2 + clip.w) * progress)
            return (x, int(H * 0.35))
        return clip.with_position(pos)

    def slide_in_right(clip, delay=0):
        def pos(t):
            if t < delay:
                return (W, int(H * 0.82))
            progress = min(1.0, (t - delay) / 0.8)
            x = int(W - (W // 2 - clip.w // 2 + clip.w) * progress)
            return (x, int(H * 0.82))
        return clip.with_position(pos)

    title_clip = TextClip(
        text=script_data["title"], font_size=Config.TITLE_FONT_SIZE,
        color="white", font=font_path, text_align="center",
        size=(W - 200, None), method="caption",
    ).with_duration(main_duration)
    title_clip = slide_in_left(title_clip, delay=0.5)

    subscribe = TextClip(
        text="▶ SUBSCRIBE NOW", font_size=32,
        color=(255, 215, 0), font=font_path,
    ).with_duration(main_duration)
    subscribe = slide_in_right(subscribe, delay=1.0)

    watermark_path = os.path.join(Config.OUTPUT_DIR, "watermark.png")
    if not os.path.exists(watermark_path):
        create_watermark(watermark_path)
    try:
        wm = ImageClip(watermark_path, duration=main_duration).with_position((20, 20)).with_opacity(0.7)
        overlays.append(wm)
    except Exception:
        pass

    def make_ticker(text, duration, W, H, font_path, speed=100):
        full_text = text * 3
        tc = TextClip(text=full_text, font_size=20, color="white", font=font_path)
        tw = tc.w
        def pos(t):
            x = W - int(speed * t) % (tw // 3 + W)
            return (x, H - 30)
        return tc.with_position(pos).with_duration(duration)

    ticker_bg = ColorClip(size=(W, 35), color=(200, 30, 30), duration=main_duration).with_position((0, H - 35))
    ticker_text = make_ticker(
        "⚽ FIFA WORLD CUP 2026  •  SUBSCRIBE NOW  •  DAILY FOOTBALL NEWS  •  ",
        main_duration, W, H, font_path, speed=80
    )
    overlays.extend([ticker_bg, ticker_text])

    title_bg = ColorClip(size=(W, 100), color=(0, 0, 0), duration=main_duration).with_position((0, int(H * 0.30))).with_opacity(0.6)
    overlays.append(title_bg)

    overlays.append(title_shadow)
    overlays.append(title_clip)
    overlays.append(subscribe)

    if os.path.exists(MUSIC_PATH):
        music = AudioFileClip(MUSIC_PATH).with_duration(main_duration).with_effects([afx.MultiplyVolume(0.08)])
        final_audio = CompositeAudioClip([audio, music])
    else:
        final_audio = audio

    all_clips = [main_video] + overlays
    main_part = CompositeVideoClip(all_clips).with_audio(final_audio)

    final_parts = [intro_clip, main_part, outro_clip]
    final_video = concatenate_videoclips(final_parts, method="compose")

    final_video.write_videofile(
        output_path, fps=Config.FPS, codec="libx264", audio_codec="aac",
        preset="ultrafast", threads=2, ffmpeg_params=["-crf", "24"],
    )

    final_video.close()
    audio.close()
    for p in img_paths:
        if os.path.exists(p):
            os.remove(p)
    for p in [VOICE_PATH, INTRO_PATH, OUTRO_PATH]:
        if os.path.exists(p):
            os.remove(p)

    return output_path, THUMB_PATH
