import random
import re
from datetime import datetime

TEMPLATES = [
    {
        "title": "FIFA WORLD CUP 2026: Everything You Need To Know!",
        "description": "The biggest sporting event on Earth is almost here! Get the complete guide to the FIFA World Cup 2026 including host cities, schedule, teams, and what to expect.\n\nSUBSCRIBE for daily World Cup updates!\nLIKE if you are excited for the World Cup!\n\n#worldcup2026 #fifa #worldcup #football #soccer #fifaworldcup #2026worldcup #canada #mexico #usa #footballnews #sports",
        "tags": ["worldcup2026", "fifa", "worldcup", "football", "soccer", "fifaworldcup", "2026worldcup", "canada", "mexico", "usa", "footballnews", "sports"],
    },
    {
        "title": "World Cup 2026 Host Cities: Complete Stadium Tour!",
        "description": "Take a tour of all 16 host cities across USA, Canada, and Mexico for the 2026 FIFA World Cup. Which stadiums are ready and what fans can expect.\n\nSUBSCRIBE for more World Cup content!\n\n#worldcup2026 #fifa #worldcup #stadiums #canada #mexico #usa #soccer #football #worldcuppreview",
        "tags": ["worldcup2026", "fifa", "worldcup", "stadiums", "canada", "mexico", "usa", "soccer", "football", "worldcuppreview"],
    },
    {
        "title": "World Cup 2026 Qualifiers: Who Has Qualified So Far?",
        "description": "Tracking every team that has secured their spot in the 2026 FIFA World Cup. Updated list of qualified nations and the remaining qualification battles.\n\nSUBSCRIBE to stay updated!\n\n#worldcup2026 #qualifiers #fifa #worldcup #football #soccer #worldcupqualifiers #internationalfootball",
        "tags": ["worldcup2026", "qualifiers", "fifa", "worldcup", "football", "soccer", "worldcupqualifiers", "internationalfootball"],
    },
    {
        "title": "World Cup 2026 Format Changes: What's New?",
        "description": "The 2026 World Cup introduces a new 48-team format. We explain how it works, the new group stage structure, and what it means for fans and players.\n\nSUBSCRIBE for World Cup news!\n\n#worldcup2026 #fifa #worldcup #format #48teams #soccer #football #worldcupnews #sports",
        "tags": ["worldcup2026", "fifa", "worldcup", "format", "48teams", "soccer", "football", "worldcupnews", "sports"],
    },
    {
        "title": "Stars Set To Shine At World Cup 2026!",
        "description": "The biggest names in football preparing for the 2026 World Cup. From Messi to Mbappe, who will dominate the tournament?\n\nSUBSCRIBE for daily football updates!\n\n#worldcup2026 #fifa #worldcup #messi #mbappe #ronaldo #football #soccer #footballstars #worldcupstars",
        "tags": ["worldcup2026", "fifa", "worldcup", "messi", "mbappe", "ronaldo", "football", "soccer", "footballstars", "worldcupstars"],
    },
    {
        "title": "World Cup 2026 Favorites: Who Will Lift The Trophy?",
        "description": "Expert predictions for the 2026 FIFA World Cup. We analyze the top contenders, dark horses, and make our case for who will be crowned champions.\n\nSUBSCRIBE for predictions and analysis!\n\n#worldcup2026 #fifa #worldcup #predictions #favorites #soccer #football #worldcuppredictions #champions",
        "tags": ["worldcup2026", "fifa", "worldcup", "predictions", "favorites", "soccer", "football", "worldcuppredictions", "champions"],
    },
    {
        "title": "Today's Football News Roundup + World Cup 2026 Updates",
        "description": "The latest football news from around the globe including World Cup 2026 preparations, transfer updates, and match results.\n\nSUBSCRIBE so you never miss a video!\n\n#footballnews #worldcup2026 #soccer #football #premierleague #laliga #seriea #bundesliga #championsleague #dailysports",
        "tags": ["footballnews", "worldcup2026", "soccer", "football", "premierleague", "laliga", "seriea", "bundesliga", "championsleague", "dailysports"],
    },
]


_EMOJI = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "\u2600-\u27BF"
    "\u2B50\u200d\u23cf\u23e9\u231a\ufe0f\u3030"
    "]+",
    re.UNICODE,
)


def clean_text(text):
    return _EMOJI.sub("", text).strip()


def generate_script(match_text, stories):
    template = random.choice(TEMPLATES)
    date_str = datetime.now().strftime("%B %d, %Y")

    intros = [
        "Welcome to Football Highlights Daily! Today is {date} and we have massive World Cup 2026 news to share.",
        "Hey football fans! It's {date} and the World Cup 2026 excitement is building! Here's what you need to know.",
        "Hello everyone! {date} here and we are bringing you the latest from the FIFA World Cup 2026 and beyond.",
    ]

    body_parts = [random.choice(intros).format(date=date_str)]

    if match_text and "no matches" not in match_text.lower():
        body_parts.append("Latest matches and updates:")
        body_parts.append(match_text)

    if stories:
        body_parts.append("Breaking football news:")
        for i, s in enumerate(stories[:4], 1):
            s_clean = clean_text(s)
            if s_clean and len(s_clean) > 15:
                body_parts.append(f"{i}. {s_clean}")

    outros = [
        "What do you think about the World Cup 2026? Which team are you supporting? Let us know in the comments! Subscribe for daily updates!",
        "The World Cup is going to be incredible! Drop your predictions in the comments and subscribe so you don't miss any of our World Cup coverage!",
        "Thanks for watching! Like and subscribe for daily football and World Cup 2026 content. See you in the next video!",
    ]

    body_parts.append(random.choice(outros))

    script = "\n\n".join(body_parts)
    script = clean_text(script)
    script = re.sub(r"\s+", " ", script).strip()

    return {
        "title": template["title"],
        "description": template["description"],
        "tags": template["tags"],
        "script": script,
    }
