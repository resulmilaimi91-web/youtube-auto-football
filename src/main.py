import os
import sys
import random
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.config import Config
from src.football_data import (
    get_todays_matches,
    get_world_cup_2026_news,
    format_match_text,
)
from src.script_generator import generate_script
from src.video_generator import create_video, STYLES
from src.youtube_uploader import upload_video, upload_short


def run_analytics_if_due():
    try:
        analytics_file = os.path.join(Config.OUTPUT_DIR, "analytics.json")
        run_analytics = False

        if not os.path.exists(analytics_file):
            run_analytics = True
        else:
            mtime = os.path.getmtime(analytics_file)
            last_run = datetime.fromtimestamp(mtime)
            hours_since = (datetime.now() - last_run).total_seconds() / 3600
            if hours_since >= 6:
                run_analytics = True

        if run_analytics:
            from src.analytics import run_analytics
            result = run_analytics()
            return result
    except Exception as e:
        print(f"Analytics error: {e}")
    return None


def run():
    print(f"[{datetime.now()}] Starting YouTube auto-upload pipeline...")

    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

    print("[1/6] Running analytics check...")
    analytics = run_analytics_if_due()

    print("[2/6] Fetching World Cup 2026 & football news...")
    matches = get_todays_matches()
    wc_news = get_world_cup_2026_news()
    match_text = format_match_text(matches)

    all_stories = wc_news
    print(f"  Found {len(matches)} matches, {len(wc_news)} World Cup stories")

    print("[3/6] Generating long-form video script...")
    script_data = generate_script(match_text, all_stories)
    print(f"  Title: {script_data['title']}")

    style = random.choice(STYLES)
    print(f"  Style: {style}")

    print("[4/6] Creating professional video (12+ min)...")
    video_path = os.path.join(Config.OUTPUT_DIR, "video.mp4")
    video_path, thumb_path = create_video(script_data, video_path, style=style)
    print(f"  Video: {video_path}")

    print("[5/6] Uploading long-form video to YouTube...")
    video_url = upload_video(video_path, thumb_path, script_data)
    print(f"  Uploaded: {video_url}")

    if os.path.exists(video_path):
        os.remove(video_path)
    if os.path.exists(thumb_path):
        os.remove(thumb_path)

    print("[6/6] Generating and uploading Shorts...")
    try:
        from src.shorts_generator import generate_shorts_batch
        shorts_dir = os.path.join(Config.OUTPUT_DIR, "shorts")
        shorts = generate_shorts_batch(count=2, output_dir=shorts_dir)

        for short in shorts:
            short_url = upload_short(short["path"], short["info"])
            if short_url:
                print(f"  Short uploaded: {short_url}")
            if os.path.exists(short["path"]):
                os.remove(short["path"])
    except Exception as e:
        print(f"  Shorts generation failed: {e}")

    print(f"[{datetime.now()}] Pipeline complete! Video: {video_url}")
    return video_url


if __name__ == "__main__":
    run()
