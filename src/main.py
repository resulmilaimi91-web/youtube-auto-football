import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.config import Config
from src.football_data import get_todays_matches, get_top_stories, format_match_text
from src.script_generator import generate_script
from src.video_generator import create_video
from src.youtube_uploader import upload_video

def run():
    print(f"[{datetime.now()}] Starting YouTube auto-upload pipeline...")

    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

    print("[1/4] Fetching football data...")
    matches = get_todays_matches()
    stories = get_top_stories()
    match_text = format_match_text(matches)
    print(f"  Found {len(matches)} matches, {len(stories)} stories")

    print("[2/4] Generating script...")
    script_data = generate_script(match_text, stories)
    print(f"  Title: {script_data['title']}")

    print("[3/4] Creating video...")
    video_path = os.path.join(Config.OUTPUT_DIR, "video.mp4")
    video_path, thumb_path = create_video(script_data, video_path)
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
