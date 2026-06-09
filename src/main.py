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
from src.youtube_uploader import upload_video


def run():
    print(f"[{datetime.now()}] Starting YouTube auto-upload pipeline...")

    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

    print("[1/4] Fetching World Cup 2026 & football news...")
    matches = get_todays_matches()
    wc_news = get_world_cup_2026_news()
    match_text = format_match_text(matches)

    all_stories = wc_news
    print(f"  Found {len(matches)} matches, {len(wc_news)} World Cup stories")

    print("[2/4] Generating script...")
    script_data = None

    if os.environ.get("GEMINI_API_KEY"):
        try:
            from src.ai_script_generator import generate_ai_script
            script_data = generate_ai_script(match_text, all_stories)
            if script_data:
                print("  Using AI-generated script (Gemini)")
        except Exception as e:
            print(f"  AI script failed: {e}")

    if not script_data:
        script_data = generate_script(match_text, all_stories)
        print("  Using template script")

    print(f"  Title: {script_data['title']}")

    style = random.choice(STYLES)
    print(f"  Style: {style}")

    print("[3/4] Creating professional video...")
    video_path = os.path.join(Config.OUTPUT_DIR, "video.mp4")
    video_path, thumb_path = create_video(script_data, video_path, style=style)
    print(f"  Video: {video_path}")

    print("[4/4] Uploading to YouTube...")
    video_url = upload_video(video_path, thumb_path, script_data)
    print(f"  Uploaded: {video_url}")

    if os.path.exists(video_path):
        os.remove(video_path)
    if os.path.exists(thumb_path):
        os.remove(thumb_path)

    print(f"[{datetime.now()}] Pipeline complete! Video: {video_url}")
    return video_url


if __name__ == "__main__":
    run()
