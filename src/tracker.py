import os
import json
from datetime import datetime, timedelta
from src.config import Config

REPORT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "progress.json")

MONETIZATION_GOALS = {
    "subscribers": 1000,
    "watch_hours": 4000,
    "shorts_views_90d": 10_000_000,
}


def load_progress():
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r") as f:
            return json.load(f)
    return {"days": [], "last_run": None}


def save_progress(data):
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_youtube_stats():
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request

        creds = Credentials(
            token=None,
            refresh_token=Config.YOUTUBE_REFRESH_TOKEN,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=Config.YOUTUBE_CLIENT_ID,
            client_secret=Config.YOUTUBE_CLIENT_SECRET,
            scopes=["https://www.googleapis.com/auth/youtube"],
        )
        creds.refresh(Request())

        youtube = build("youtube", "v3", credentials=creds)

        channel = youtube.channels().list(part="statistics,snippet", mine=True).execute()
        stats = channel["items"][0]["statistics"]
        snippet = channel["items"][0]["snippet"]

        subscriber_count = int(stats.get("subscriberCount", 0))
        view_count = int(stats.get("viewCount", 0))
        video_count = int(stats.get("videoCount", 0))
        channel_name = snippet.get("title", "Unknown")

        return {
            "subscribers": subscriber_count,
            "total_views": view_count,
            "videos": video_count,
            "channel_name": channel_name,
            "error": None,
        }
    except Exception as e:
        return {"error": str(e)}


def get_shorts_stats():
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request

        creds = Credentials(
            token=None,
            refresh_token=Config.YOUTUBE_REFRESH_TOKEN,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=Config.YOUTUBE_CLIENT_ID,
            client_secret=Config.YOUTUBE_CLIENT_SECRET,
            scopes=["https://www.googleapis.com/auth/youtube"],
        )
        creds.refresh(Request())

        youtube = build("youtube", "v3", credentials=creds)

        total_shorts_views = 0
        next_page = None
        cutoff = datetime.now() - timedelta(days=90)

        while True:
            request = youtube.search().list(
                part="id,snippet",
                forMine=True,
                type="video",
                videoDuration="short",
                maxResults=50,
                pageToken=next_page,
            )
            response = request.execute()

            for item in response.get("items", []):
                published = datetime.fromisoformat(
                    item["snippet"]["publishedAt"].replace("Z", "+00:00")
                )
                if published < cutoff:
                    continue
                video_id = item["id"]["videoId"]
                try:
                    vstats = youtube.videos().list(
                        part="statistics", id=video_id
                    ).execute()
                    if vstats["items"]:
                        total_shorts_views += int(
                            vstats["items"][0]["statistics"].get("viewCount", 0)
                        )
                except Exception:
                    pass

            next_page = response.get("nextPageToken")
            if not next_page:
                break

        total_watch_hours = 0
        next_page = None
        while True:
            request = youtube.search().list(
                part="id,snippet",
                forMine=True,
                type="video",
                maxResults=50,
                pageToken=next_page,
            )
            response = request.execute()

            for item in response.get("items", []):
                video_id = item["id"]["videoId"]
                try:
                    vstats = youtube.videos().list(
                        part="statistics,contentDetails", id=video_id
                    ).execute()
                    if vstats["items"]:
                        duration_str = vstats["items"][0]["contentDetails"]["duration"]
                        import isodate
                        duration_sec = isodate.parse_duration(duration_str).total_seconds()
                        views = int(vstats["items"][0]["statistics"].get("viewCount", 0))
                        total_watch_hours += (duration_sec * views) / 3600
                except Exception:
                    pass

            next_page = response.get("nextPageToken")
            if not next_page:
                break

        return {
            "shorts_views_90d": total_shorts_views,
            "watch_hours": total_watch_hours,
            "error": None,
        }
    except Exception as e:
        return {"error": str(e)}


def run():
    print(f"[{datetime.now()}] YouTube Progress Tracker")
    print("=" * 60)

    stats = get_youtube_stats()
    if stats.get("error"):
        print(f"Error getting stats: {stats['error']}")
        return

    data = load_progress()
    today = datetime.now().strftime("%Y-%m-%d")
    last_run = data.get("last_run", "")

    shorts_stats = get_shorts_stats()

    entry = {
        "date": today,
        "subscribers": stats["subscribers"],
        "total_views": stats["total_views"],
        "videos": stats["videos"],
        "shorts_views_90d": shorts_stats.get("shorts_views_90d", 0),
        "watch_hours": round(shorts_stats.get("watch_hours", 0), 1),
    }

    if not data["days"] or data["days"][-1]["date"] != today:
        data["days"].append(entry)
    else:
        data["days"][-1] = entry

    if last_run:
        last_entry = data["days"][-2] if len(data["days"]) > 1 else entry
        subs_gained = stats["subscribers"] - last_entry.get("subscribers", stats["subscribers"])
        views_gained = stats["total_views"] - last_entry.get("total_views", stats["total_views"])
    else:
        subs_gained = 0
        views_gained = 0

    data["last_run"] = today
    save_progress(data)

    print(f"Channel: {stats['channel_name']}")
    print(f"Videos: {stats['videos']}")
    print(f"Subscribers: {stats['subscribers']} ({'+' if subs_gained >= 0 else ''}{subs_gained})")
    print(f"Total Views: {stats['total_views']} ({'+' if views_gained >= 0 else ''}{views_gained})")
    print(f"Shorts Views (90d): {shorts_stats.get('shorts_views_90d', 0):,}")
    print(f"Watch Hours: {shorts_stats.get('watch_hours', 0):.1f}")
    print()

    pct_subs = min(100, stats["subscribers"] / MONETIZATION_GOALS["subscribers"] * 100)
    pct_watch = min(100, (shorts_stats.get("watch_hours", 0) or 0) / MONETIZATION_GOALS["watch_hours"] * 100)
    pct_shorts = min(100, (shorts_stats.get("shorts_views_90d", 0) or 0) / MONETIZATION_GOALS["shorts_views_90d"] * 100)

    print("MONETIZATION PROGRESS:")
    print(f"  Subscribers: {stats['subscribers']}/{MONETIZATION_GOALS['subscribers']} ({pct_subs:.1f}%)")
    print(f"  Watch Hours: {shorts_stats.get('watch_hours', 0):.1f}/{MONETIZATION_GOALS['watch_hours']} ({pct_watch:.1f}%)")
    print(f"  Shorts Views (90d): {shorts_stats.get('shorts_views_90d', 0):,}/{MONETIZATION_GOALS['shorts_views_90d']:,} ({pct_shorts:.4f}%)")
    print()

    if stats["subscribers"] >= 1000 and (shorts_stats.get("watch_hours", 0) >= 4000 or shorts_stats.get("shorts_views_90d", 0) >= 10_000_000):
        print("STATUS: MONETIZATION ELIGIBLE! Apply at youtube.com/monetize")
    else:
        print("STATUS: Building momentum. Keep posting!")

    print("=" * 60)


if __name__ == "__main__":
    run()
