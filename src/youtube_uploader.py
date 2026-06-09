import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from src.config import Config

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]

def _make_client_config():
    return {
        "installed": {
            "client_id": Config.YOUTUBE_CLIENT_ID,
            "client_secret": Config.YOUTUBE_CLIENT_SECRET,
            "redirect_uris": ["http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

def get_authenticated_service():
    creds = None
    token_path = os.path.join(Config.OUTPUT_DIR, "token.pickle")
    os.makedirs(os.path.dirname(token_path), exist_ok=True)

    if os.path.exists(token_path):
        with open(token_path, "rb") as f:
            creds = pickle.load(f)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        if Config.YOUTUBE_REFRESH_TOKEN:
            creds = Credentials(
                token=None,
                refresh_token=Config.YOUTUBE_REFRESH_TOKEN,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=Config.YOUTUBE_CLIENT_ID,
                client_secret=Config.YOUTUBE_CLIENT_SECRET,
                scopes=SCOPES,
            )
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(_make_client_config(), SCOPES)
            creds = flow.run_local_server(port=8080, prompt="consent")

        with open(token_path, "wb") as f:
            pickle.dump(creds, f)

    return build("youtube", "v3", credentials=creds)

def upload_video(video_path, thumb_path, script_data):
    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": script_data["title"],
            "description": script_data["description"],
            "tags": script_data["tags"],
            "categoryId": "17",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media,
        )
        response = request.execute()
        video_id = response["id"]

        if os.path.exists(thumb_path):
            try:
                youtube.thumbnails().set(
                    videoId=video_id,
                    media_body=MediaFileUpload(thumb_path),
                ).execute()
            except HttpError as thumb_err:
                print(f"Thumbnail upload skipped (not allowed for this account): {thumb_err}")

        return f"https://youtube.com/watch?v={video_id}"
    except HttpError as e:
        print(f"YouTube upload error (continuing): {e}")
        return None


def upload_short(video_path, script_data):
    youtube = get_authenticated_service()

    title = script_data.get("title", "Football Shorts #shorts")
    if "#shorts" not in title.lower():
        title += " #shorts"

    body = {
        "snippet": {
            "title": title,
            "description": script_data.get("script", "") + "\n\n#shorts #football #worldcup2026 #soccer #fifa",
            "tags": script_data.get("hashtags", ["shorts", "football", "worldcup2026"]),
            "categoryId": "17",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media,
        )
        response = request.execute()
        video_id = response["id"]
        return f"https://youtube.com/shorts/{video_id}"
    except HttpError as e:
        print(f"Short upload error (continuing): {e}")
        return None
