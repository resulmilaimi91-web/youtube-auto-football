import os
import json
from datetime import datetime

PLAYLIST_CACHE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "playlist_cache.json")


def _get_youtube():
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from src.config import Config

    creds = Credentials(
        token=None,
        refresh_token=Config.YOUTUBE_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=Config.YOUTUBE_CLIENT_ID,
        client_secret=Config.YOUTUBE_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/youtube"],
    )
    creds.refresh(Request())
    return build("youtube", "v3", credentials=creds)


def _load_cache():
    if os.path.exists(PLAYLIST_CACHE):
        with open(PLAYLIST_CACHE, "r") as f:
            return json.load(f)
    return {}


def _save_cache(data):
    os.makedirs(os.path.dirname(PLAYLIST_CACHE), exist_ok=True)
    with open(PLAYLIST_CACHE, "w") as f:
        json.dump(data, f, indent=2)


def _get_or_create_playlist(youtube, theme):
    cache = _load_cache()
    if theme in cache:
        try:
            resp = youtube.playlists().list(part="id", id=cache[theme]).execute()
            if resp.get("items"):
                return cache[theme]
        except Exception:
            pass

    titles = {
        "abc": "ABC & Alphabet Songs",
        "numbers": "Counting & Numbers Songs",
        "shapes": "Shapes Learning Songs",
        "colors": "Colors & Rainbow Songs",
        "rainbow": "Colors & Rainbow Songs",
        "train": "Fun Train Songs",
        "stars": "Counting & Numbers Songs",
        "bunny": "Animal Songs for Kids",
        "fish": "Animal Songs for Kids",
        "cat": "Animal Songs for Kids",
        "morning": "Daily Routine Songs",
        "days": "Days of the Week Songs",
        "body": "Body Parts Songs",
        "fruits": "Healthy Eating Songs",
        "weather": "Weather & Nature Songs",
        "vehicles": "Vehicles & Transportation Songs",
        "animals": "Animal Songs for Kids",
    }

    playlist_title = titles.get(theme, f"{theme.title()} Songs for Kids")
    desc = f"Fun and educational {playlist_title.lower()} for toddlers and preschoolers! Made with love by Cortana Kids Songs."

    try:
        body = {"snippet": {"title": playlist_title, "description": desc}, "status": {"privacyStatus": "public"}}
        resp = youtube.playlists().insert(part="snippet,status", body=body).execute()
        pid = resp["id"]
        cache[theme] = pid
        _save_cache(cache)
        return pid
    except Exception:
        return None


def add_video_to_playlist(youtube, video_id, theme):
    if not video_id or not theme:
        return False
    playlist_id = _get_or_create_playlist(youtube, theme)
    if not playlist_id:
        return False
    try:
        body = {"snippet": {"playlistId": playlist_id, "resourceId": {"kind": "youtube#video", "videoId": video_id}}}
        youtube.playlistItems().insert(part="snippet", body=body).execute()
        return True
    except Exception:
        return False


def add_video_to_all_playlists(video_id, theme):
    try:
        youtube = _get_youtube()
        return add_video_to_playlist(youtube, video_id, theme)
    except Exception:
        return False
