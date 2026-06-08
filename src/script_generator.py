import random
import re
from datetime import datetime

TEMPLATES = [
    {
        "title": "INSANE Goals This Week Will Leave You Speechless!",
        "description": "From 30-yard rockets to bicycle kicks -- we've compiled the most INSANE goals from around the world. Premier League, La Liga, Serie A, Bundesliga and more!\n\nSUBSCRIBE for daily football content!\nLIKE if you enjoyed the video!\nCOMMENT your favorite goal!\n\n#football #soccer #goals #premierleague #laliga #seriea #bundesliga #championsleague #footballhighlights #worldcup2026 #footballnews #sports",
        "tags": ["football", "soccer", "goals", "premierleague", "laliga", "seriea", "bundesliga", "championsleague", "footballhighlights", "worldcup2026", "footballnews", "sports"],
    },
    {
        "title": "SHOCKING Result Nobody Expected! Premier League Drama",
        "description": "The biggest upset of the season just happened. Full breakdown of the match that has everyone talking. Tactical analysis, key moments, and post-match reactions.\n\nSUBSCRIBE for more football updates!\nHit LIKE to support the channel!\n\n#premierleague #football #soccer #epl #matchanalysis #footballnews #sports #upset #england #premierleaguehighlights",
        "tags": ["premierleague", "epl", "football", "soccer", "matchanalysis", "footballnews", "upset", "sports", "england", "premierleaguehighlights"],
    },
    {
        "title": "Today's Football Roundup: EVERYTHING You Missed!",
        "description": "Busy day? We've got you covered. Here's every goal, every card, every big moment from today's football action across all major leagues.\n\nSUBSCRIBE so you never miss a video!\nLIKE to help the channel grow!\nCOMMENT your team below!\n\n#footballnews #football #soccer #highlights #dailysports #sportsnews #premierleague #laliga #seriea #bundesliga #championsleague #worldcup2026",
        "tags": ["footballnews", "football", "soccer", "dailysports", "sportsnews", "premierleague", "laliga", "seriea", "bundesliga", "championsleague", "worldcup2026"],
    },
    {
        "title": "BREAKING: Major Transfer Confirmed - Here's What We Know",
        "description": "The transfer window is heating up! We break down the latest confirmed deal including fee, contract length, medical details, and what this means for both clubs.\n\nSUBSCRIBE for transfer news FIRST!\nLIKE to stay updated!\n\n#transfers #footballtransfernews #soccer #premierleague #laliga #transferwindow #footballnews #transferrumors #breakingnews #transfers2026",
        "tags": ["transfers", "footballtransfernews", "soccer", "premierleague", "laliga", "transferwindow", "transferrumors", "footballnews", "breakingnews", "transfers2026"],
    },
    {
        "title": "UNBELIEVABLE Record Broken - History Made!",
        "description": "A historic moment in football just happened. We analyze the record-breaking performance, compare it to legends of the game, and explain why this is so special.\n\nSUBSCRIBE for more incredible content!\nDROP A LIKE for the record-breaker!\n\n#footballrecords #soccerstars #goals #premierleague #championsleague #football #history #recordbreaking #footballhistory #sports",
        "tags": ["footballrecords", "soccerstars", "goals", "premierleague", "championsleague", "football", "history", "recordbreaking", "sports", "worldcup2026"],
    },
    {
        "title": "DEEP DIVE: Match Analysis You Won't See on TV",
        "description": "Professional tactical breakdown of the biggest match. Formations, pressing traps, counter-attacking patterns, and key individual battles -- explained simply.\n\nSUBSCRIBE for expert analysis!\nLIKE if you learned something!\n\n#matchanalysis #footballhighlights #socceranalysis #premierleague #tactics #football #soccer #analysis #footballtactics #footballanalysis",
        "tags": ["matchanalysis", "footballhighlights", "socceranalysis", "premierleague", "tactics", "football", "soccer", "analysis", "footballtactics", "footballanalysis"],
    },
    {
        "title": "Next SUPERSTAR? These Young Talents Are INCREDIBLE",
        "description": "The future of football is bright. We profile the most exciting young players in Europe right now -- their stats, playing style, and potential.\n\nSUBSCRIBE to discover future stars!\nLIKE to support young talent!\n\n#youngtalents #risingstars #football #soccer #premierleague #laliga #seriea #bundesliga #futurestars #footballprodigy",
        "tags": ["youngtalents", "risingstars", "football", "soccer", "premierleague", "laliga", "seriea", "bundesliga", "futurestars", "footballprodigy"],
    },
    {
        "title": "Premier League WRAP: Every Goal and Talking Point",
        "description": "Full Premier League roundup! All the goals, controversial decisions, fan reactions, and what it means for the table. Your one-stop EPL recap.\n\nSUBSCRIBE for PL content every week!\nLIKE for the Premier League!\n\n#premierleague #epl #football #goals #soccer #england #footballhighlights #premierleaguehighlights #matchday #eplhighlights",
        "tags": ["premierleague", "epl", "football", "goals", "soccer", "england", "footballhighlights", "premierleaguehighlights", "matchday", "sports"],
    },
    {
        "title": "Champions League Nights Are BACK! Best Moments",
        "description": "The UEFA Champions League delivered another unforgettable night of football drama. We bring you every goal, save, and celebration from matchday.\n\nSUBSCRIBE for UCL content!\nLIKE for European nights!\n\n#championsleague #ucl #football #goals #europe #soccer #uefachampionsleague #championsleaguehighlights #uclhighlights #football",
        "tags": ["championsleague", "ucl", "football", "goals", "europe", "soccer", "uefachampionsleague", "championsleaguehighlights", "uclhighlights", "football"],
    },
    {
        "title": "MIND-BLOWING Football Facts You Never Knew!",
        "description": "These incredible football statistics and stories will completely change how you see the beautiful game. Some of these are almost unbelievable!\n\nSUBSCRIBE for more amazing content!\nLIKE for football trivia!\n\n#footballfacts #soccerfacts #trivia #football #soccer #interestingfacts #didyouknow #footballtrivia #sportsfacts #footballknowledge",
        "tags": ["footballfacts", "soccerfacts", "trivia", "football", "soccer", "interestingfacts", "didyouknow", "footballtrivia", "sportsfacts", "footballknowledge"],
    },
    {
        "title": "SACKED! Another Manager Leaves - What Went Wrong?",
        "description": "The managerial merry-go-round continues. We analyze why this manager lost his job, what went wrong tactically, and who could replace him.\n\nSUBSCRIBE for football news!\nLIKE if you agree with the decision!\n\n#footballmanagers #sackrace #premierleague #soccernews #footballnews #manager #sacking #coaching #tactics #footballmanager",
        "tags": ["footballmanagers", "sackrace", "premierleague", "soccernews", "footballnews", "manager", "sacking", "coaching", "tactics", "footballmanager"],
    },
    {
        "title": "FANS WENT CRAZY! Best Stadium Moments This Week",
        "description": "The best atmosphere, tifos, celebrations, and fan moments from stadiums around the world. This is what makes football the beautiful game.\n\nSUBSCRIBE for fan culture content!\nLIKE if you love the atmosphere!\n\n#footballfans #stadiumatmosphere #soccer #football #fans #tifo #atmosphere #footballculture #ultras #matchday",
        "tags": ["footballfans", "stadiumatmosphere", "soccer", "football", "fans", "tifo", "atmosphere", "footballculture", "ultras", "matchday"],
    },
    {
        "title": "Transfer Window: EVERY Deal Confirmed So Far",
        "description": "Complete transfer tracker with all confirmed deals, fees, contract details, and expert analysis on whether each signing is a bargain or overpriced.\n\nSUBSCRIBE for transfer updates!\nLIKE to support the channel!\n\n#transfers #transferwindow #footballnews #soccer #premierleague #laliga #seriea #bundesliga #transfernews #summertransfers",
        "tags": ["transfers", "transferwindow", "footballnews", "soccer", "premierleague", "laliga", "seriea", "bundesliga", "transfernews", "summertransfers"],
    },
    {
        "title": "The GREATEST Underdog Story in Football",
        "description": "This is the most inspiring football story you'll hear all year. How a team written off by everyone defied impossible odds to achieve greatness.\n\nSUBSCRIBE for incredible stories!\nLIKE to support underdogs!\n\n#underdog #footballstory #inspiration #soccer #football #comeback #sportsstory #inspiring #motivation #nevergiveup",
        "tags": ["underdog", "footballstory", "inspiration", "soccer", "football", "comeback", "sportsstory", "inspiring", "motivation", "nevergiveup"],
    },
    {
        "title": "WORST MISSES of the Week! How Did They Miss?!",
        "description": "From open goals to penalty blunders -- these shocking misses will have you laughing and crying at the same time. Worst finishing ever!\n\nSUBSCRIBE for more football fun!\nLIKE if you could have scored these!\n\n#funnyfootball #misses #soccerfails #footballfails #comedy #footballshorts #funnymoments #sportscomedy #footballfunny #fail",
        "tags": ["funnyfootball", "misses", "soccerfails", "footballfails", "comedy", "footballshorts", "funnymoments", "sportscomedy", "footballfunny", "fail"],
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
        "Welcome back to Football Highlights Daily! Today is {date} and we have an action-packed update for you.",
        "Hey football fans! It's {date} and we're bringing you the latest from the world of football.",
        "What's going on everyone? {date} here and the football world is buzzing with excitement!",
        "Hello and welcome! It's {date} and we've got some massive football news to share with you today.",
    ]

    body_parts = [random.choice(intros).format(date=date_str)]

    if match_text and "no matches" not in match_text.lower():
        body_parts.append("Today's fixtures:")
        body_parts.append(match_text)

    if stories:
        body_parts.append("Top football stories:")
        for i, s in enumerate(stories[:3], 1):
            s_clean = clean_text(s)
            if s_clean:
                body_parts.append(f"{i}. {s_clean}")

    outros = [
        "What do you think about today's news? Drop your thoughts in the comments below! Don't forget to subscribe and hit that bell icon for daily football updates!",
        "Which story caught your attention the most? Let us know in the comments! Subscribe now so you never miss another video!",
        "Thanks for watching! If you enjoyed this update, smash that like button and subscribe for more football content every day!",
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
