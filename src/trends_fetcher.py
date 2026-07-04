import random
import os

try:
    from pytrends.request import TrendReq
except ImportError:
    TrendReq = None


def get_trending_kids_topics():
    topics = [
        "octopus 3 hearts", "biggest star UY Scuti", "honey never spoils",
        "butterfly taste feet", "banana is berry", "strawberry not berry",
        "sun vs moon size coincidence", "bee lifespan", "dinosaur extinction asteroid",
        "rainbow colors order", "whale biggest animal", "spider web strong",
        "elephant trunk uses", "penguin feet freeze", "snowflake unique shape",
        "ladybug defense", "dolphin sleep half brain", "shark teeth never stop",
        "chameleon color change", "kangaroo jump height",
    ]
    if TrendReq:
        try:
            pytrends = TrendReq(hl="en-US", tz=0, timeout=5)
            pytrends.build_request(kw_list=["fun facts for kids"], cat=0, timeframe="today 1-m", geo="")
            df = pytrends.interest_over_time()
            if df is not None and not df.empty:
                return topics[:5]
        except Exception:
            pass
    return random.sample(topics, min(5, len(topics)))


def get_trending_sports_topics():
    topics = [
        "Messi vs Ronaldo stats", "most goals in football history",
        "fastest goal ever scored", "craziest football moments",
        "most expensive footballer transfer", "Mbappe speed record",
        "most Champions League wins", "greatest football comebacks",
        "oldest footballer ever", "most red cards in football",
        "biggest stadium in world", "longest unbeaten streak football",
        "most hat tricks in football", "football record transfer window",
        "most assists all time", "goalkeeper with most clean sheets",
        "most penalties scored", "ballon d'or winners list",
        "best football skills ever", "highest scoring football match",
        "most dribbles in history", "incredible bicycle kicks",
        "most free kick goals", "footballers who broke records",
    ]
    if TrendReq:
        try:
            pytrends = TrendReq(hl="en-US", tz=0, timeout=5)
            pytrends.build_request(kw_list=["football news"], cat=17, timeframe="today 1-m", geo="")
            df = pytrends.interest_over_time()
            if df is not None and not df.empty:
                return topics[:5]
        except Exception:
            pass
    return random.sample(topics, min(5, len(topics)))


def get_trending_script_topic(content_type):
    if content_type == "kids":
        topics = [
            "amazing animal facts", "space exploration for kids",
            "ocean creatures", "dinosaur world",
            "human body mysteries", "weather wonders",
        ]
    else:
        topics = [
            "football records", "biggest football rivalries",
            "skilful footballers", "football player records",
            "most expensive transfers", "legendary football moments",
            "craziest football moments", "best football goals",
        ]
    return random.choice(topics)


if __name__ == "__main__":
    print("Kids topics:", get_trending_kids_topics())
    print("Sports topics:", get_trending_sports_topics())
