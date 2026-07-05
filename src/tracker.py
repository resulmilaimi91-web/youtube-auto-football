import os
import json
from datetime import datetime, timedelta
from src.config import Config

REPORT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "progress.json")
STRATEGY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content_strategy.json")

MONETIZATION_GOALS = {
    "subscribers": 1000,
    "watch_hours": 4000,
    "shorts_views_90d": 10_000_000,
}


def _get_youtube():
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
    return build("youtube", "v3", credentials=creds)


def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def get_channel_stats(youtube):
    channel = youtube.channels().list(part="statistics,snippet", mine=True).execute()
    stats = channel["items"][0]["statistics"]
    snippet = channel["items"][0]["snippet"]
    return {
        "subscribers": int(stats.get("subscriberCount", 0)),
        "total_views": int(stats.get("viewCount", 0)),
        "videos": int(stats.get("videoCount", 0)),
        "channel_name": snippet.get("title", "Unknown"),
    }


def get_video_performance(youtube):
    videos = []
    next_page = None
    while True:
        resp = youtube.search().list(
            part="id,snippet",
            forMine=True,
            type="video",
            maxResults=50,
            pageToken=next_page,
        ).execute()
        for item in resp.get("items", []):
            vid = item["id"]["videoId"]
            title = item["snippet"]["title"]
            published = item["snippet"]["publishedAt"]
            try:
                vstats = youtube.videos().list(part="statistics,contentDetails", id=vid).execute()
                if vstats["items"]:
                    s = vstats["items"][0]["statistics"]
                    cd = vstats["items"][0]["contentDetails"]["duration"]
                    import isodate
                    dur_sec = isodate.parse_duration(cd).total_seconds()
                    is_short = dur_sec <= 60
                    videos.append({
                        "id": vid,
                        "title": title,
                        "views": int(s.get("viewCount", 0)),
                        "likes": int(s.get("likeCount", 0)),
                        "comments": int(s.get("commentCount", 0)),
                        "published": published,
                        "is_short": is_short,
                        "score": int(s.get("viewCount", 0)) + int(s.get("likeCount", 0)) * 5,
                    })
            except Exception:
                pass
        next_page = resp.get("nextPageToken")
        if not next_page:
            break
    videos.sort(key=lambda v: v["score"], reverse=True)
    return videos


def analyze_best_themes(videos, strategy):
    all_themes = [
        "rainbow", "bunny", "stars", "fish", "train", "cat", "morning",
    ]
    for v in videos:
        title_lower = v["title"].lower()
        matched = None
        for theme in all_themes:
            if theme in title_lower:
                matched = theme
                break
        if matched is None:
            for theme in all_themes:
                if theme in title_lower.split():
                    matched = theme
                    break
        if matched and v["views"] > 0:
            if matched not in strategy["theme_scores"]:
                strategy["theme_scores"][matched] = {"total_views": 0, "count": 0, "total_score": 0}
            strategy["theme_scores"][matched]["total_views"] += v["views"]
            strategy["theme_scores"][matched]["count"] += 1
            strategy["theme_scores"][matched]["total_score"] += v["score"]

    for theme in strategy["theme_scores"]:
        t = strategy["theme_scores"][theme]
        t["avg_views"] = t["total_views"] / max(t["count"], 1)
        t["avg_score"] = t["total_score"] / max(t["count"], 1)

    strategy["best_theme"] = max(
        strategy["theme_scores"],
        key=lambda t: strategy["theme_scores"][t]["avg_score"] if strategy["theme_scores"][t]["count"] > 0 else 0,
    ) if strategy["theme_scores"] else None

    strategy["theme_rankings"] = sorted(
        strategy["theme_scores"].keys(),
        key=lambda t: strategy["theme_scores"][t]["avg_score"],
        reverse=True,
    )
    return strategy


def recommend_next_topic(strategy):
    best = strategy.get("best_theme")
    rankings = strategy.get("theme_rankings", [])
    if rankings:
        top3 = rankings[:3]
        strategy["recommended_themes"] = top3
        strategy["recommendation_note"] = (
            f"Based on performance, prioritize: {', '.join(top3)}"
        )
    else:
        strategy["recommended_themes"] = ["rainbow", "stars", "cat"]
        strategy["recommendation_note"] = "Not enough data yet. Cycling through all themes."
    return strategy


def run():
    print(f"[{datetime.now()}] YouTube Progress Tracker + Content Optimizer")
    print("=" * 60)

    try:
        youtube = _get_youtube()
    except Exception as e:
        print(f"Auth failed: {e}")
        return

    stats = get_channel_stats(youtube)
    videos = get_video_performance(youtube)

    progress = load_json(REPORT_FILE)
    today = datetime.now().strftime("%Y-%m-%d")

    shorts_views = sum(v["views"] for v in videos if v["is_short"] and
                       (datetime.now() - datetime.fromisoformat(v["published"].replace("Z", "+00:00"))).days <= 90)
    watch_hours = round(sum(
        (datetime.now() - datetime.fromisoformat(v["published"].replace("Z", "+00:00"))).total_seconds() / 3600 * 0.1
        for v in videos if not v["is_short"]
    ), 1)

    entry = {
        "date": today,
        "subscribers": stats["subscribers"],
        "total_views": stats["total_views"],
        "videos": stats["videos"],
        "shorts_views_90d": shorts_views,
        "watch_hours": watch_hours,
    }

    days = progress.get("days", [])
    if not days or days[-1]["date"] != today:
        days.append(entry)
    else:
        days[-1] = entry
    progress["days"] = days
    progress["last_run"] = today
    save_json(REPORT_FILE, progress)

    strategy = load_json(STRATEGY_FILE)
    if "theme_scores" not in strategy:
        strategy["theme_scores"] = {}
    strategy = analyze_best_themes(videos, strategy)
    strategy = recommend_next_topic(strategy)
    strategy["last_analysis"] = today
    save_json(STRATEGY_FILE, strategy)

    print(f"Channel: {stats['channel_name']}")
    print(f"Subscribers: {stats['subscribers']}")
    print(f"Total Views: {stats['total_views']}")
    print(f"Videos: {stats['videos']}")
    print(f"Shorts Views (90d): {shorts_views:,}")
    print(f"Watch Hours: {watch_hours:.1f}")
    print()

    pct_subs = min(100, stats["subscribers"] / MONETIZATION_GOALS["subscribers"] * 100) if MONETIZATION_GOALS["subscribers"] else 0
    pct_watch = min(100, watch_hours / MONETIZATION_GOALS["watch_hours"] * 100) if MONETIZATION_GOALS["watch_hours"] else 0

    print("MONETIZATION PROGRESS:")
    print(f"  Subscribers: {stats['subscribers']}/{MONETIZATION_GOALS['subscribers']} ({pct_subs:.1f}%)")
    print(f"  Watch Hours: {watch_hours:.1f}/{MONETIZATION_GOALS['watch_hours']} ({pct_watch:.1f}%)")
    print(f"  Shorts Views (90d): {shorts_views:,}/{MONETIZATION_GOALS['shorts_views_90d']:,}")
    print()

    if stats["subscribers"] >= 1000 and (watch_hours >= 4000 or shorts_views >= 10_000_000):
        print("STATUS: MONETIZATION ELIGIBLE!")
    else:
        print("STATUS: Building momentum. Keep posting!")
    print()

    print("TOP PERFORMING VIDEOS:")
    for v in videos[:5]:
        tag = " [SHORT]" if v["is_short"] else ""
        print(f"  {v['views']:>5} views - {v['title'][:60]}{tag}")
    print()

    print("THEME PERFORMANCE RANKING:")
    rankings = strategy.get("theme_rankings", [])
    if rankings:
        for i, theme in enumerate(rankings[:5]):
            ts = strategy["theme_scores"].get(theme, {})
            avg = ts.get("avg_views", 0)
            print(f"  {i+1}. {theme.title():<12} avg {avg:.0f} views/video")
    print()

    print(f"RECOMMENDATION: {strategy.get('recommendation_note', 'No data yet')}")
    print(f"Next focus themes: {', '.join(strategy.get('recommended_themes', []))}")
    print("=" * 60)


if __name__ == "__main__":
    run()
