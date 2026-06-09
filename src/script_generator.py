import random
import re
from datetime import datetime

MONETIZATION_TAGS = [
    "football", "soccer", "worldcup2026", "fifa",
    "premierleague", "laliga", "seriea", "bundesliga",
    "championsleague", "footballhighlights", "footballnews",
    "goals", "highlights", "sports", "football2026",
]

TEMPLATES = [
    {
        "title": "FIFA WORLD CUP 2026: Complete Guide To The Biggest Event!",
        "description": "The FIFA World Cup 2026 is coming to USA, Canada, and Mexico! Here is everything you need to know about the biggest sporting event on Earth.\n\nSUBSCRIBE for daily World Cup updates!\nLIKE to support the channel!\nCOMMENT your favorite team!\n\n#worldcup2026 #fifa #worldcup #football #soccer #fifaworldcup #2026worldcup #canada #mexico #usa #footballnews #sports #worldcuphighlights #footballhighlights",
        "tags": ["worldcup2026", "fifa", "worldcup", "football", "soccer", "fifaworldcup", "2026worldcup", "canada", "mexico", "usa", "footballnews", "sports", "worldcuphighlights", "footballhighlights"],
        "hashtags": ["worldcup2026", "fifa", "worldcup", "football", "soccer"],
    },
    {
        "title": "World Cup 2026 Host Cities: Full Stadium Tour!",
        "description": "Take a complete tour of all 16 host cities for the 2026 FIFA World Cup. From MetLife Stadium to Estadio Azteca, which venue is the best?\n\nSUBSCRIBE for more World Cup content!\nLIKE for the stadiums!\n\n#worldcup2026 #stadiums #fifa #worldcup #canada #mexico #usa #soccer #football #worldcupstadiums #worldcuppreview",
        "tags": ["worldcup2026", "stadiums", "fifa", "worldcup", "canada", "mexico", "usa", "soccer", "football", "worldcupstadiums", "worldcuppreview"],
        "hashtags": ["worldcup2026", "stadiums", "fifa", "worldcup", "football"],
    },
    {
        "title": "World Cup 2026: Every Team That Has Qualified!",
        "description": "Updated list of all teams that have qualified for the 2026 FIFA World Cup. Who is in, who is out, and who still has a chance?\n\nSUBSCRIBE to stay updated!\nLIKE to support your team!\n\n#worldcup2026 #qualifiers #fifa #worldcup #football #soccer #worldcupqualifiers #internationalfootball #qualification",
        "tags": ["worldcup2026", "qualifiers", "fifa", "worldcup", "football", "soccer", "worldcupqualifiers", "internationalfootball"],
        "hashtags": ["worldcup2026", "qualifiers", "fifa", "worldcup", "football"],
    },
    {
        "title": "World Cup 2026: New 48-Team Format Explained!",
        "description": "The 2026 World Cup features 48 teams for the first time ever. We break down the new format, group stages, and how it affects every team.\n\nSUBSCRIBE for World Cup news!\nLIKE for the format explainer!\n\n#worldcup2026 #fifa #worldcup #format #48teams #soccer #football #worldcupnews #newformat #tournament",
        "tags": ["worldcup2026", "fifa", "worldcup", "format", "48teams", "soccer", "football", "worldcupnews", "newformat", "tournament"],
        "hashtags": ["worldcup2026", "format", "fifa", "worldcup", "football"],
    },
    {
        "title": "Top 10 Players Who Will Dominate World Cup 2026!",
        "description": "From Mbappe to Haaland, Bellingham to Vinicius, these are the players who will light up the 2026 FIFA World Cup. Who is your pick?\n\nSUBSCRIBE for daily football content!\nLIKE for the top players!\n\n#worldcup2026 #fifa #worldcup #mbappe #haaland #bellingham #football #soccer #footballstars #worldcupstars #worldclass",
        "tags": ["worldcup2026", "fifa", "worldcup", "mbappe", "haaland", "bellingham", "football", "soccer", "footballstars", "worldcupstars"],
        "hashtags": ["worldcup2026", "football", "mbappe", "fifa", "worldcup"],
    },
    {
        "title": "World Cup 2026: Who Will Win The Trophy?",
        "description": "Expert predictions for the 2026 FIFA World Cup. We analyze the favorites, dark horses, and make our case for who will lift the trophy.\n\nSUBSCRIBE for predictions and analysis!\nLIKE for your favorite team!\n\n#worldcup2026 #fifa #worldcup #predictions #favorites #soccer #football #worldcuppredictions #champions #winner",
        "tags": ["worldcup2026", "fifa", "worldcup", "predictions", "favorites", "soccer", "football", "worldcuppredictions", "champions"],
        "hashtags": ["worldcup2026", "predictions", "fifa", "worldcup", "football"],
    },
    {
        "title": "Today's Football News + World Cup 2026 Updates!",
        "description": "The latest football news from around the globe including World Cup 2026 preparations, transfer updates, and match results.\n\nSUBSCRIBE so you never miss a video!\nLIKE to help the channel grow!\n\n#footballnews #worldcup2026 #soccer #football #premierleague #laliga #seriea #bundesliga #championsleague #dailysports #footballhighlights",
        "tags": ["footballnews", "worldcup2026", "soccer", "football", "premierleague", "laliga", "seriea", "bundesliga", "championsleague", "dailysports", "footballhighlights"],
        "hashtags": ["footballnews", "worldcup2026", "football", "soccer", "highlights"],
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
        "Welcome back to Football Highlights Daily. Today is {date}, and we have massive World Cup 2026 news to share with you.",
        "Hey there, football fans. It is {date}, and the World Cup 2026 excitement is building every single day. Here is what you need to know.",
        "Good morning, everyone. {date} here, and we are bringing you the very latest from the FIFA World Cup 2026 and beyond.",
        "What is going on, football fans? It is {date}, and we are here with your daily dose of World Cup 2026 updates and analysis.",
        "Hello and welcome. Today is {date}, and we have got a packed show for you with all the latest World Cup 2026 developments.",
    ]

    body_parts = [random.choice(intros).format(date=date_str)]

    if match_text and "no matches" not in match_text.lower():
        body_parts.append("Let us start with the latest matches and updates from around the world.")
        body_parts.append(match_text)

    if stories:
        body_parts.append("Now, let us move on to the breaking football news of the day.")
        for i, s in enumerate(stories[:4], 1):
            s_clean = clean_text(s)
            if s_clean and len(s_clean) > 15:
                body_parts.append(f"Story number {i}. {s_clean}")

    outros = [
        "So, what do you think about the World Cup 2026? Which team are you backing to go all the way? Let us know your thoughts in the comments below. And if you enjoyed this video, make sure to subscribe and hit that bell icon so you never miss an update.",
        "The World Cup is going to be absolutely incredible this time around. Drop your predictions in the comments section and subscribe to our channel so you do not miss any of our World Cup coverage throughout the tournament.",
        "That is all for today, folks. If you found this helpful, please give us a like, subscribe to the channel, and hit the notification bell. We will see you in the next video with more World Cup 2026 content. Take care.",
    ]

    body_parts.append(random.choice(outros))

    script = " ".join(body_parts)
    script = clean_text(script)
    script = re.sub(r"\s+", " ", script).strip()

    return {
        "title": template["title"],
        "description": template["description"],
        "tags": template["tags"],
        "hashtags": template["hashtags"],
        "script": script,
    }
