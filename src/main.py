import os
import sys
import random
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.config import Config
from src.youtube_uploader import upload_video, upload_short
CONTENT_TYPE = os.environ.get("CONTENT_TYPE", "kids")

if CONTENT_TYPE == "fifa":
    from src.fifa_script_generator import generate_script
    from src.video_generator import create_video, STYLES
    from src.fifa_shorts import generate_viral_shorts
else:
    from src.script_generator import generate_script
    from src.kids_video_generator import create_kids_video
    from src.viral_shorts import generate_viral_shorts

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


def run():
    print(f"[{datetime.now()}] Starting YouTube auto-upload pipeline (type={CONTENT_TYPE})...")

    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

    can_upload = _check_upload_quota()

    print("[1/5] Generating long-form video script...")
    script_data = generate_script()
    print(f"  Title: {script_data['title']}")

    video_url = None
    if can_upload:
        print("[2/5] Creating video...")
        video_path = os.path.join(Config.OUTPUT_DIR, "video.mp4")
        if CONTENT_TYPE == "kids":
            video_path, thumb_path = create_kids_video(script_data, video_path)
        else:
            style = random.choice(STYLES) if STYLES else "modern"
            print(f"  Style: {style}")
            video_path, thumb_path = create_video(script_data, video_path, style=style)
        print(f"  Video: {video_path}")

        print("[3/5] Uploading long-form video to YouTube...")
        video_url = upload_video(video_path, thumb_path, script_data)
        print(f"  Uploaded: {video_url}")

        if video_url == "QUOTA_EXCEEDED":
            _record_upload_fail()
            print("  [QUOTA] Upload limit recorded, will skip uploads for 12h")
            video_url = None

        for p in [video_path, thumb_path]:
            if os.path.exists(p):
                os.remove(p)
    else:
        print("[2/5] Skipping video generation (upload quota)")
        print("[3/5] Skipping upload (quota)")

    print("[4/5] Generating viral Shorts...")
    try:
        shorts_dir = os.path.join(Config.OUTPUT_DIR, "shorts")
        shorts = generate_viral_shorts(output_dir=shorts_dir)

        if can_upload:
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
    except Exception as e:
        print(f"  Shorts generation failed: {e}")

    print(f"[{datetime.now()}] Pipeline complete!")
    return video_url


if __name__ == "__main__":
    run()
