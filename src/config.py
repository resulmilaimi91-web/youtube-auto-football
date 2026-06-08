import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
    YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
    YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "")

    CHANNEL_NAME = os.getenv("CHANNEL_NAME", "Football Highlights Daily")
    UPLOAD_SCHEDULE_HOURS = int(os.getenv("UPLOAD_SCHEDULE_HOURS") or "6")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

    VIDEO_WIDTH = 1920
    VIDEO_HEIGHT = 1080
    TITLE_FONT_SIZE = 72
    SUBTITLE_FONT_SIZE = 48
    FOOTER_FONT_SIZE = 36
    FPS = 24
