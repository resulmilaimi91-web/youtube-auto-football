import requests
import random
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import urllib.request

FOOTBALL_API_URL = "https://www.thesportsdb.com/api/v1/json/3"

PORTALS = [
    "https://www.bbc.com/sport/football",
    "https://www.espn.com/soccer/",
    "https://www.skysports.com/football",
    "https://www.goal.com/en",
]


def fetch_portal_news():
    headlines = []
    for portal in PORTALS:
        try:
            html = requests.get(portal, timeout=8, headers={"User-Agent": "Mozilla/5.0"}).text
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup.select("h2, h3, a"):
                t = tag.get_text(strip=True)
                if t and 20 < len(t) < 150:
                    headlines.append(t)
        except Exception:
            pass
        if len(headlines) > 20:
            break
    return headlines[:10]


def get_world_cup_2026_news():
    world_cup_keywords = ["world cup", "worldcup", "world cup 2026", "fifa", "2026 world cup"]
    all_news = fetch_portal_news()
    wc_news = [n for n in all_news if any(k in n.lower() for k in world_cup_keywords)]
    return wc_news[:5] if wc_news else all_news[:5]


def get_todays_matches():
    date = datetime.now().strftime("%Y-%m-%d")
    url = f"{FOOTBALL_API_URL}/eventsday.php?d={date}"
    try:
        resp = requests.get(url, timeout=10).json()
        return resp.get("events", []) or []
    except Exception:
        return []


def get_world_cup_matches():
    try:
        url = f"{FOOTBALL_API_URL}/searchteams.php?t=World%20Cup"
        resp = requests.get(url, timeout=10).json()
        return resp.get("teams", []) or []
    except Exception:
        return []


def format_match_text(matches, is_world_cup=False):
    if not matches:
        if is_world_cup:
            return "The FIFA World Cup 2026 is coming! Stay tuned for the biggest football event on the planet."
        return "No major matches today. But the football world never sleeps!"

    prefix = "FIFA World Cup 2026" if is_world_cup else "Today's"
    lines = [f"{prefix} - Latest Updates:"]
    for m in matches[:5]:
        home = m.get("strHomeTeam", "?")
        away = m.get("strAwayTeam", "?")
        league = m.get("strLeague", "?")
        time = m.get("strTime", "?")
        lines.append(f"{home} vs {away} | {league} at {time}")
    return "\n".join(lines)


def download_football_images(count=3):
    urls = []
    try:
        from_image = f"https://source.unsplash.com/1920x1080/?football,soccer,stadium"
        for i in range(count):
            url = f"https://source.unsplash.com/1920x1080/?football,soccer,stadium,goal,worldcup&sig={i}"
            urls.append(url)
    except Exception:
        pass
    return urls
