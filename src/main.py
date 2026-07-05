import os
import sys
import random
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.config import Config
CONTENT_TYPE = os.environ.get("CONTENT_TYPE", "kids")

if CONTENT_TYPE == "fifa":
    from src.fifa_script_generator import generate_script
    from src.video_generator import create_video, STYLES
    from src.fifa_shorts import generate_viral_shorts
else:
    from src.kids_song_generator import generate_song
    from src.kids_animation_generator import create_kids_song_video
    from src.fifa_shorts import generate_viral_shorts

QUOTA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "upload_quota.json")


def _check_upload_quota():
    if os.path.exists(QUOTA_FILE):
        try:
            with open(QUOTA_FILE, "r") as f:
                data = json.load(f)
            last_fail = datetime.fromisoformat(data.get("last_fail", "2000-01-01"))
            hours_since = (datetime.now() - last_fail).total_seconds() / 3600
            if hours_since < 12:
                print(f"  [QUOTA] Upload limit hit {hours_since:.1f}h ago, skipping upload (retry in {12 - hours_since:.1f}h)")
                return False
        except Exception:
            pass
    return True


def _record_upload_fail():
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    with open(QUOTA_FILE, "w") as f:
        json.dump({"last_fail": datetime.now().isoformat()}, f)


def _clear_upload_quota():
    if os.path.exists(QUOTA_FILE):
        os.remove(QUOTA_FILE)


def _generate_voiceover(script_text, output_path):
    try:
        import edge_tts
        import asyncio

        voice = "en-US-AriaNeural"
        if CONTENT_TYPE == "kids":
            voice = "en-US-JennyNeural"

        async def _run():
            tts = edge_tts.Communicate(script_text, voice=voice, rate="+10%", pitch="+5%")
            await tts.save(output_path)
        asyncio.run(_run())
        if os.path.getsize(output_path) > 1000:
            return
    except Exception as e:
        print(f"  edge-tts failed: {e}")

    try:
        from gtts import gTTS
        tts = gTTS(text=script_text, lang="en", slow=False, tld="com")
        tts.save(output_path)
        if os.path.getsize(output_path) > 1000:
            return
    except Exception as e2:
        print(f"  gTTS failed: {e2}")
        with open(output_path, "wb") as f:
            f.write(b"")


def run():
    print(f"[{datetime.now()}] Starting YouTube auto-upload pipeline (type={CONTENT_TYPE})...")

    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

    can_upload = _check_upload_quota()

    print("[1/5] Generating content...")
    if CONTENT_TYPE == "kids":
        script_data = generate_song()
        print(f"  Song: {script_data['title']}")
    else:
        script_data = generate_script()
        print(f"  Title: {script_data['title']}")

    video_url = None
    if can_upload:
        print("[2/5] Creating video...")
        video_path = os.path.join(Config.OUTPUT_DIR, "video.mp4")
        voice_path = os.path.join(Config.OUTPUT_DIR, "voiceover.mp3")

        print("  Generating voiceover...")
        if CONTENT_TYPE == "kids":
            _generate_voiceover("\n".join(script_data["lyrics"]), voice_path)
        else:
            _generate_voiceover(script_data["script"], voice_path)

        if CONTENT_TYPE == "kids":
            video_path, thumb_path = create_kids_song_video(script_data, video_path, voice_path)
        else:
            style = random.choice(STYLES) if STYLES else "modern"
            print(f"  Style: {style}")
            video_path, thumb_path = create_video(script_data, video_path, style=style)

        print(f"  Video: {video_path}")

        print("[3/5] Uploading to YouTube...")
        from src.youtube_uploader import upload_video
        video_url = upload_video(video_path, thumb_path, script_data)
        print(f"  Uploaded: {video_url}")

        if video_url == "QUOTA_EXCEEDED":
            _record_upload_fail()
            print("  [QUOTA] Upload limit recorded, will skip uploads for 12h")
            video_url = None

        for p in [video_path, thumb_path, voice_path]:
            if os.path.exists(p):
                os.remove(p)
    else:
        print("[2/5] Skipping video generation (upload quota)")
        print("[3/5] Skipping upload (quota)")

    print("[4/5] Generating Shorts...")
    if CONTENT_TYPE == "kids":
        from src.viral_shorts import generate_viral_shorts
        shorts_dir = os.path.join(Config.OUTPUT_DIR, "shorts")
        try:
            shorts = generate_viral_shorts(output_dir=shorts_dir)
        except Exception as e:
            print(f"  Kids shorts generation failed: {e}")
            shorts = []
    else:
        shorts_dir = os.path.join(Config.OUTPUT_DIR, "shorts")
        try:
            shorts = generate_viral_shorts(output_dir=shorts_dir)
        except Exception as e:
            print(f"  FIFA shorts generation failed: {e}")
            shorts = []

    if can_upload:
        from src.youtube_uploader import upload_short
        for short in shorts:
            short_url = upload_short(short["path"], short["info"])
            if short_url == "QUOTA_EXCEEDED":
                _record_upload_fail()
                print("  [QUOTA] Upload limit hit during Shorts, stopping")
                break
            elif short_url:
                print(f"  Short uploaded: {short_url}")
            if os.path.exists(short["path"]):
                os.remove(short["path"])
    else:
        print("  Skipping Shorts upload (quota)")

    return video_url


if __name__ == "__main__":
    run()
