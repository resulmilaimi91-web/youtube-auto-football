import random
from datetime import datetime

TEMPLATES = [
    {
        "title": "Today's Football News You Can't Miss! ⚽",
        "description": "The latest football updates, top goals, transfer news, and match analysis from around the world. Stay informed!",
        "tags": ["football", "soccer", "highlights", "goals", "premierleague", "laliga", "seriea", "bundesliga", "championsleague", "footballnews"],
    },
    {
        "title": "Top 5 Goals of the Week That Will Blow Your Mind! 🔥",
        "description": "The most spectacular goals from Premier League, La Liga, Serie A, Bundesliga, and more. Watch and enjoy!",
        "tags": ["topgoals", "footballhighlights", "soccer", "goals", "premierleague", "laliga", "footballshorts"],
    },
    {
        "title": "What Happened Today in the Football World? ⚡",
        "description": "A complete roundup of today's biggest football stories, match results, and breaking news. Subscribe for daily updates!",
        "tags": ["footballnews", "football", "soccer", "highlights", "sportsnews", "dailysports"],
    },
    {
        "title": "Breaking: Major Transfer News & Match Analysis 📰",
        "description": "Latest transfer rumors, confirmed deals, and expert match analysis. Everything you need to know about the beautiful game.",
        "tags": ["transfers", "footballtransfernews", "soccer", "premierleague", "transferrumors"],
    },
]

def generate_script(match_text, stories):
    template = random.choice(TEMPLATES)
    date_str = datetime.now().strftime("%B %d, %Y")

    body_parts = [f"Hello football fans! Today is {date_str} and we have some exciting news from the world of football."]

    if match_text and "no matches" not in match_text.lower():
        body_parts.append("\nToday's matches:")
        body_parts.append(match_text)

    if stories:
        body_parts.append("\nTop stories:")
        for i, s in enumerate(stories[:3], 1):
            body_parts.append(f"{i}. {s}")

    body_parts.append("\nWhat do you think about these updates? Let us know in the comments below!")
    body_parts.append("Don't forget to subscribe and hit the bell icon so you never miss an update!")

    script = "\n\n".join(body_parts)
    return {
        "title": template["title"],
        "description": template["description"] + f"\n\n📅 {date_str}\n\n🔔 Subscribe for daily football updates!\n\n#football #soccer #highlights #footballnews",
        "tags": template["tags"],
        "script": script,
    }
