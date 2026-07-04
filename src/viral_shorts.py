import os
import random
import urllib.request
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from moviepy import (
    ImageClip, AudioFileClip, concatenate_videoclips,
)
from moviepy.audio.fx import AudioFadeIn, AudioFadeOut
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


def _download_picsum(path, seed):
    try:
        url = f"https://picsum.photos/seed/{seed}/1080/1920"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=15).read()
        if len(data) > 5000:
            with open(path, "wb") as f:
                f.write(data)
            return True
    except Exception:
        pass
    return False


def _get_kids_images(theme_idx):
    seeds = [
        ["kids_space_1", "kids_animal_1", "kids_ocean_1", "kids_dinosaur_1"],
        ["kids_rainbow_1", "kids_butterfly_1", "kids_planet_1", "kids_fruit_1"],
        ["kids_sun_1", "kids_tree_1", "kids_fish_1", "kids_star_1"],
    ]
    seed_list = seeds[theme_idx % len(seeds)]
    images = []
    for seed in seed_list:
        path = os.path.join(Config.OUTPUT_DIR, f"kids_img_{seed}.jpg")
        ok = _download_picsum(path, seed)
        if ok:
            img = Image.open(path).convert("RGB")
            img = img.resize((1080, 1920), Image.LANCZOS)
            images.append(img)
    if not images:
        img = Image.new("RGB", (1080, 1920), (100, 150, 255))
        draw = ImageDraw.Draw(img)
        for y in range(0, 1920, 5):
            for x in range(0, 1080, 5):
                c = random.randint(0, 2)
                draw.point((x, y), fill=(random.randint(50,255), random.randint(50,255), random.randint(50,255)))
        images.append(img)
    return images


KIDS_FACTS = [
    {
        "title": "Did You Know? Octopus has 3 hearts! #shorts #kids #funfacts",
        "script": "Did you know an octopus has three hearts? Two pump blood to the gills, one pumps it to the body. And when they swim, the heart that pumps to the body stops! That's why they prefer to crawl. Amazing, right?",
        "bg": [(100, 150, 255), (50, 100, 200)],
        "text": (255, 255, 255),
        "accent": (255, 215, 0),
        "hooks": ["WAIT, WHAT?!", "MIND-BLOWING!", "NO WAY!"],
    },
    {
        "title": "Space Fact: Stars are GIANT! #shorts #kids #space",
        "script": "Did you know the biggest star in the universe is called UY Scuti? It is so huge that if it were our sun, it would swallow everything up to the planet Saturn! Our sun is tiny compared to it!",
        "bg": [(20, 20, 80), (50, 30, 120)],
        "text": (255, 255, 255),
        "accent": (255, 200, 50),
        "hooks": ["STOP SCROLLING!", "THAT'S HUGE!", "INCREDIBLE!"],
    },
    {
        "title": "Honey never spoils! #shorts #kids #nature",
        "script": "Did you know honey never goes bad? Archaeologists found 3000-year-old honey in Egyptian tombs and it was still perfectly good to eat! Honey is the only food that lasts forever!",
        "bg": [(200, 150, 50), (150, 100, 30)],
        "text": (255, 255, 255),
        "accent": (255, 215, 0),
        "hooks": ["AMAZING!", "THAT'S OLD!", "WOW!"],
    },
    {
        "title": "Bananas are berries, but strawberries aren't! #shorts #kids",
        "script": "Did you know bananas are technically berries, but strawberries are NOT? A berry has seeds inside, not outside. So bananas qualify, but strawberries don't! Science is so weird!",
        "bg": [(255, 200, 50), (200, 150, 30)],
        "text": (255, 255, 255),
        "accent": (255, 100, 100),
        "hooks": ["WHAT?!", "THAT'S CRAZY!", "NO WAY!"],
    },
    {
        "title": "Butterflies taste with their feet! #shorts #kids #animals",
        "script": "Did you know butterflies taste food with their feet? They have taste sensors on their legs! When they land on a flower, they taste it immediately. Cool, right?",
        "bg": [(150, 200, 255), (100, 150, 200)],
        "text": (255, 255, 255),
        "accent": (255, 100, 200),
        "hooks": ["REALLY?!", "THAT'S WILD!", "AMAZING!"],
    },
    {
        "title": "The Sun is 400 times bigger! #shorts #kids #science",
        "script": "Did you know the Sun is 400 times bigger than the Moon? But it also is 400 times farther away. That's why they look the same size in the sky! Perfect cosmic coincidence!",
        "bg": [(255, 150, 50), (200, 100, 30)],
        "text": (255, 255, 255),
        "accent": (255, 255, 100),
        "hooks": ["COSMIC!", "WOW!", "INCREDIBLE!"],
    },
]

KIDS_VIDEOS = [
    {
        "title": "Fun Facts for Smart Kids! #shorts #kids #learning",
        "script": "Here are amazing facts every smart kid should know. Animals, space, science - learn something new every day! Subscribe for more fun facts!",
        "bg": [(50, 200, 100), (30, 150, 70)],
        "text": (255, 255, 255),
        "accent": (255, 215, 0),
        "hooks": ["FUN TIME!", "LEARN THIS!", "COOL FACTS!"],
    },
]


def _create_kids_frame(W, H, theme, hook_text, bg_image, part=0):
    img = bg_image.copy()
    img = img.resize((W, H), Image.LANCZOS)

    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.45)

    img = img.filter(ImageFilter.GaussianBlur(radius=3))

    draw = ImageDraw.Draw(img)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)

    ov_draw.rectangle([0, 100, W, 600], fill=(0, 0, 0, 160))
    ov_draw.rectangle([0, H - 300, W, H - 100], fill=(0, 0, 0, 160))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    font_huge = _get_font(100)
    font_hook = _get_font(70)
    font_big = _get_font(50)
    font_small = _get_font(30)

    hook_y = 70
    bbox = draw.textbbox((0, 0), hook_text, font=font_hook)
    tw = bbox[2] - bbox[0]
    draw.text((W // 2 - tw // 2 + 3, hook_y + 3), hook_text, fill=(0, 0, 0), font=font_hook)
    draw.text((W // 2 - tw // 2, hook_y), hook_text, fill=theme["accent"], font=font_hook)

    cx, cy = W // 2, H // 2 + 50
    draw.ellipse([cx - 130, cy - 130, cx + 130, cy + 130], fill=(0, 0, 0, 180))
    draw.ellipse([cx - 125, cy - 125, cx + 125, cy + 125], outline=theme["accent"], width=5)
    draw.polygon([(cx - 45, cy - 60), (cx - 45, cy + 60), (cx + 65, cy)], fill=theme["accent"])

    draw.rectangle([60, H - 250, W - 60, H - 140], fill=(255, 50, 50))
    bbox_sub = draw.textbbox((0, 0), "SUBSCRIBE FOR KIDS!", font=font_big)
    tw_sub = bbox_sub[2] - bbox_sub[0]
    draw.text((W // 2 - tw_sub // 2, H - 235), "SUBSCRIBE FOR KIDS!", fill=(255, 255, 255), font=font_big)

    draw.rectangle([0, 0, W, 8], fill=theme["accent"])
    draw.rectangle([0, H - 8, W, H], fill=theme["accent"])

    return img


def create_kids_short(theme_idx, output_path, voice_path=None):
    from src.config import Config
    theme = KIDS_FACTS[theme_idx % len(KIDS_FACTS)]
    W, H = 1080, 1920
    part_duration = 4

    bg_images = _get_kids_images(theme_idx)

    frames = []
    for part in range(2):
        hook = theme["hooks"][part % len(theme["hooks"])]
        bg_img = bg_images[part % len(bg_images)]
        frame = _create_kids_frame(W, H, theme, hook, bg_img, part)
        frame_path = output_path.replace(".mp4", f"_part{part}.png")
        frame.save(frame_path, quality=95)
        frames.append(frame_path)

    clips = []
    for i, frame_path in enumerate(frames):
        clip = ImageClip(frame_path, duration=part_duration)
        clip = clip.with_effects([AudioFadeIn(0.3), AudioFadeOut(0.3)])
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
        "hashtags": ["shorts", "kids", "funfacts", "learning", "education"],
    }


def generate_viral_shorts(output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(Config.OUTPUT_DIR, "shorts")
    os.makedirs(output_dir, exist_ok=True)

    results = []
    for i in range(1):
        output_path = os.path.join(output_dir, f"kids_short_{i+1}.mp4")
        try:
            path, info = create_kids_short(i, output_path)
            results.append({"path": path, "info": info})
            print(f"  Kids Short {i+1}: {info['title'][:50]}...")
        except Exception as e:
            print(f"  Kids Short {i+1} failed: {e}")

    return results


if __name__ == "__main__":
    results = generate_viral_shorts()
    for r in results:
        print(f"\nKids Short: {r['info']['title']}")
        print(f"  Duration: {r['info']['duration']}s")
        print(f"  Path: {r['path']}")
