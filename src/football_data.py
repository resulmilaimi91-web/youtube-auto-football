import requests
from datetime import datetime, timedelta

FOOTBALL_API_URL = "https://www.thesportsdb.com/api/v1/json/3"

def get_todays_matches():
    date = datetime.now().strftime("%Y-%m-%d")
    url = f"{FOOTBALL_API_URL}/eventsday.php?d={date}"
    try:
        resp = requests.get(url, timeout=10).json()
        return resp.get("events", []) or []
    except:
        return []

def get_top_stories():
    headlines = []
    try:
        from bs4 import BeautifulSoup
        html = requests.get("https://www.bbc.com/sport/football", timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        for h in soup.select("h2, h3"):
            t = h.get_text(strip=True)
            if t and len(t) > 20:
                headlines.append(t)
    except:
        pass
    return headlines[:5]

def format_match_text(matches):
    if not matches:
        return "Sot nuk ka ndeshje të mëdha futbolli. Por përgatituni për spektaklin e radhës!"

    lines = ["Lajmet e fundit nga bota e futbollit:"]
    for m in matches[:5]:
        home = m.get("strHomeTeam", "?")
        away = m.get("strAwayTeam", "?")
        league = m.get("strLeague", "?")
        time = m.get("strTime", "?")
        lines.append(f"{home} vs {away} - {league}, ora {time}")
    return "\n".join(lines)
