import os
import json
from datetime import datetime, timedelta


ANALYTICS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "analytics.json")


def fetch_channel_analytics():
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials

        api_key = os.environ.get("YOUTUBE_API_KEY", "")
        refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN", "")
        client_id = os.environ.get("YOUTUBE_CLIENT_ID", "")
        client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET", "")
        channel_name = os.environ.get("CHANNEL_NAME", "")

        if not api_key:
            return None

        credentials = None
        if refresh_token and client_id and client_secret:
            credentials = Credentials(
                token=None,
                refresh_token=refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=client_id,
                client_secret=client_secret,
            )

        if credentials:
            youtube = build("youtube", "v3", credentials=credentials)
            channel_response = youtube.channels().list(
                part="statistics,snippet",
                mine=True
            ).execute()
        else:
            youtube = build("youtube", "v3", developerKey=api_key)
            if channel_name:
                channel_response = youtube.channels().list(
                    part="statistics,snippet",
                    forUsername=channel_name
                ).execute()
            else:
                return None

        if not channel_response.get("items"):
            return None

        channel = channel_response["items"][0]
        stats = channel["statistics"]
        channel_id = channel["id"]

        videos_response = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            order="date",
            maxResults=20,
            type="video"
        ).execute()

        videos = []
        for item in videos_response.get("items", []):
            video_id = item["id"]["videoId"]
            try:
                video_stats = youtube.videos().list(
                    part="statistics",
                    id=video_id
                ).execute()

                if video_stats.get("items"):
                    vs = video_stats["items"][0]["statistics"]
                    videos.append({
                        "id": video_id,
                        "title": item["snippet"]["title"],
                        "published": item["snippet"]["publishedAt"],
                        "views": int(vs.get("viewCount", 0)),
                        "likes": int(vs.get("likeCount", 0)),
                        "comments": int(vs.get("commentCount", 0)),
                    })
            except Exception:
                continue

        return {
            "channel": {
                "subscribers": int(stats.get("subscriberCount", 0)),
                "total_views": int(stats.get("viewCount", 0)),
                "total_videos": int(stats.get("videoCount", 0)),
            },
            "videos": videos,
            "fetched_at": datetime.now().isoformat(),
        }

    except Exception as e:
        print(f"Analytics fetch failed: {e}")
        return None


def analyze_performance(data):
    if not data or not data.get("videos"):
        return None

    videos = data["videos"]
    total_views = sum(v["views"] for v in videos)
    total_likes = sum(v["likes"] for v in videos)
    total_comments = sum(v["comments"] for v in videos)
    avg_views = total_views // max(len(videos), 1)
    avg_likes = total_likes // max(len(videos), 1)

    top_videos = sorted(videos, key=lambda x: x["views"], reverse=True)[:5]
    worst_videos = sorted(videos, key=lambda x: x["views"])[:3]

    engagement_rate = (total_likes + total_comments) / max(total_views, 1) * 100

    return {
        "summary": {
            "total_views": total_views,
            "avg_views": avg_views,
            "avg_likes": avg_likes,
            "engagement_rate": round(engagement_rate, 2),
            "total_videos": len(videos),
            "subscribers": data["channel"]["subscribers"],
        },
        "top_performers": top_videos,
        "underperformers": worst_videos,
    }


def generate_suggestions(analytics):
    if not analytics:
        return []

    suggestions = []
    summary = analytics["summary"]
    top = analytics.get("top_performers", [])
    worst = analytics.get("underperformers", [])

    if summary["avg_views"] < 100:
        suggestions.append({
            "type": "titles",
            "priority": "high",
            "message": "Views are low (avg <100). Test more clickbait-style titles with ALL CAPS, numbers, and emotional words like 'SHOCKING' or 'INSANE'.",
        })

    if summary["engagement_rate"] < 2:
        suggestions.append({
            "type": "engagement",
            "priority": "high",
            "message": "Engagement rate is below 2%. Add more questions in scripts, ask viewers to comment, and create controversial opinions.",
        })

    if summary["subscribers"] < 50:
        suggestions.append({
            "type": "growth",
            "priority": "high",
            "message": "Fewer than 50 subscribers. Focus on YouTube Shorts (15-60 sec clips) to attract new viewers faster.",
        })

    if top:
        best_title = top[0].get("title", "")
        if any(w in best_title.lower() for w in ["top 10", "ranking", "best", "worst"]):
            suggestions.append({
                "type": "content",
                "priority": "medium",
                "message": "List/ranking videos perform best. Create more 'Top 10' style content.",
            })
        if any(w in best_title.lower() for w in ["breaking", "news", "update"]):
            suggestions.append({
                "type": "content",
                "priority": "medium",
                "message": "Breaking news content performs well. Post within 1 hour of major football events.",
            })

    if worst:
        for v in worst[:2]:
            suggestions.append({
                "type": "improve",
                "priority": "medium",
                "message": f"Low performer: '{v['title'][:50]}...' ({v['views']} views). Analyze what makes top videos different.",
            })

    suggestions.append({
        "type": "schedule",
        "priority": "low",
        "message": "Best posting times for football content: 12PM-2PM and 6PM-9PM UTC. Consider adjusting upload schedule.",
    })

    suggestions.append({
        "type": "thumbnails",
        "priority": "medium",
        "message": "Use bright colors (red, yellow), large text (3-5 words max), and expressive faces on thumbnails for higher CTR.",
    })

    suggestions.append({
        "type": "shorts",
        "priority": "high",
        "message": "Create YouTube Shorts from best moments of each video. Shorts get 10x more reach than regular videos.",
    })

    return suggestions


def save_analytics(data, analysis, suggestions):
    os.makedirs(os.path.dirname(ANALYTICS_FILE), exist_ok=True)

    record = {
        "timestamp": datetime.now().isoformat(),
        "raw_data": data,
        "analysis": analysis,
        "suggestions": suggestions,
    }

    history = []
    if os.path.exists(ANALYTICS_FILE):
        try:
            with open(ANALYTICS_FILE, "r") as f:
                history = json.load(f)
        except Exception:
            history = []

    history.append(record)
    history = history[-50:]

    with open(ANALYTICS_FILE, "w") as f:
        json.dump(history, f, indent=2, default=str)

    return ANALYTICS_FILE


def run_analytics():
    print("[Analytics] Fetching channel data...")
    data = fetch_channel_analytics()

    if not data:
        print("[Analytics] No data available yet")
        return None

    print(f"[Analytics] Channel: {data['channel']['subscribers']} subscribers, {data['channel']['total_views']} views")

    analysis = analyze_performance(data)
    suggestions = generate_suggestions(analysis)

    save_analytics(data, analysis, suggestions)

    if analysis:
        s = analysis["summary"]
        print(f"[Analytics] Avg views: {s['avg_views']}, Engagement: {s['engagement_rate']}%")

    if suggestions:
        print(f"[Analytics] {len(suggestions)} suggestions generated")
        for sug in suggestions[:3]:
            print(f"  [{sug['priority'].upper()}] {sug['message'][:80]}...")

    return {"data": data, "analysis": analysis, "suggestions": suggestions}


if __name__ == "__main__":
    run_analytics()
