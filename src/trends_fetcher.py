import random
import json
import urllib.request
import urllib.parse
import re
from datetime import datetime

try:
    from pytrends.request import TrendReq
    HAS_PYTRENDS = True
except ImportError:
    HAS_PYTRENDS = False


def _fetch_trending_searches(geo="US"):
    try:
        url = f"https://trends.google.com/trends/trendingsearches/daily?geo={geo}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        data = urllib.request.urlopen(req, timeout=10).read().decode()
        titles = re.findall(r'<a[^>]*class="[^"]*title[^"]*"[^>]*>(.*?)</a>', data, re.DOTALL)
        return [re.sub(r'<[^>]+>', '', t).strip() for t in titles if t.strip()][:15]
    except Exception:
        return []


def _fetch_pytrends_topics(keywords, cat=0, geo=""):
    if not HAS_PYTRENDS:
        return []
    try:
        pytrends = TrendReq(hl="en-US", tz=0, timeout=10)
        pytrends.build_request(kw_list=keywords, cat=cat, timeframe="now 7-d", geo=geo, gprop="")
        df = pytrends.interest_over_time()
        if df is not None and not df.empty:
            topics = []
            for col in df.columns:
                if col != "isPartial":
                    val = df[col].sum()
                    if val > 0:
                        topics.append((col, int(val)))
            topics.sort(key=lambda x: x[1], reverse=True)
            return [t[0] for t in topics[:5]]
    except Exception:
        pass
    return []


def _score_topic(topic, trending_searches):
    score = 0
    topic_lower = topic.lower()
    for ts in trending_searches:
        ts_lower = ts.lower()
        words = topic_lower.split()
        matches = sum(1 for w in words if w in ts_lower)
        if matches > 0:
            score += matches * 10
    return score


def get_trending_kids_topics():
    fallback = [
        "octopus 3 hearts", "biggest star UY Scuti", "honey never spoils",
        "butterfly taste feet", "banana is berry", "strawberry not berry",
        "sun vs moon size coincidence", "dinosaur extinction asteroid",
        "rainbow colors order", "whale biggest animal",
        "elephant trunk uses", "penguin feet freeze",
        "dolphin sleep half brain", "shark teeth never stop",
        "chameleon color change", "kangaroo jump height",
        "volcano eruption facts", "how planes fly", "why is sky blue",
        "fastest animal on earth", "how do bees make honey",
    ]
    trending = _fetch_trending_searches()
    pytrends_topics = _fetch_pytrends_topics(["fun facts for kids", "kids education", "amazing facts"], cat=0)
    all_trending = trending + pytrends_topics
    if not all_trending:
        return random.sample(fallback, min(5, len(fallback)))
    scored = [(t, _score_topic(t, all_trending)) for t in fallback]
    scored.sort(key=lambda x: x[1], reverse=True)
    best = [t for t, s in scored if s > 0][:5]
    if len(best) < 5:
        remaining = [t for t in fallback if t not in best]
        best.extend(random.sample(remaining, min(5 - len(best), len(remaining))))
    return best[:5]


def get_trending_sports_topics():
    fallback = [
        "Messi vs Ronaldo stats", "most goals in football history",
        "fastest goal ever scored", "craziest football moments",
        "most expensive footballer transfer", "Mbappe speed record",
        "greatest football comebacks", "most red cards in football",
        "most hat tricks in football", "football record transfer window",
        "most assists all time", "goalkeeper with most clean sheets",
        "best football skills ever", "highest scoring football match",
        "most free kick goals", "world cup 2026 predictions",
        "best young footballers 2026", "football news today",
    ]
    trending = _fetch_trending_searches()
    pytrends_topics = _fetch_pytrends_topics(["football news", "soccer highlights", "world cup 2026"], cat=17)
    all_trending = trending + pytrends_topics
    if not all_trending:
        return random.sample(fallback, min(5, len(fallback)))
    scored = [(t, _score_topic(t, all_trending)) for t in fallback]
    scored.sort(key=lambda x: x[1], reverse=True)
    best = [t for t, s in scored if s > 0][:5]
    if len(best) < 5:
        remaining = [t for t in fallback if t not in best]
        best.extend(random.sample(remaining, min(5 - len(best), len(remaining))))
    return best[:5]


def get_trending_script_topic(content_type):
    if content_type == "kids":
        topics = get_trending_kids_topics()
    else:
        topics = get_trending_sports_topics()
    selected = random.choice(topics) if topics else "trending topic"
    topic_parts = selected.split()
    return " ".join(topic_parts[:8])


if __name__ == "__main__":
    print("=" * 40)
    print(f"Kids: {get_trending_kids_topics()}")
    print(f"Kids script topic: {get_trending_script_topic('kids')}")
    print("=" * 40)
    print(f"Sports: {get_trending_sports_topics()}")
    print(f"Sports script topic: {get_trending_script_topic('fifa')}")
