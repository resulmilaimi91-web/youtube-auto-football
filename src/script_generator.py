import random
from datetime import datetime

TEMPLATES = [
    {
        "title": "INSANE Goals This Week Will Leave You Speechless! \u26bd\ufe0f",
        "description": "From 30-yard rockets to bicycle kicks \u2014 we've compiled the most INSANE goals from around the world. Premier League, La Liga, Serie A, Bundesliga & more!\n\n\ud83d\udd14 SUBSCRIBE for daily football content!\n\ud83d\udc4d LIKE if you enjoyed the video!\n\ud83d\udcac COMMENT your favorite goal!\n\n#football #soccer #goals #highlights #premierleague #laliga #seriea #bundesliga #championsleague #footballhighlights #topgoals #sports",
        "tags": ["football", "soccer", "goals", "highlights", "premierleague", "laliga", "seriea", "bundesliga", "championsleague", "topgoals", "footballhighlights", "sports"],
    },
    {
        "title": "SHOCKING Result Nobody Expected! \ud83d\ude33 Premier League Drama",
        "description": "The biggest upset of the season just happened. Full breakdown of the match that has everyone talking. Tactical analysis, key moments, and post-match reactions.\n\n\ud83d\udd14 SUBSCRIBE for more football updates!\n\ud83d\udc4d Hit LIKE to support the channel!\n\n#premierleague #football #soccer #highlights #epl #matchanalysis #footballnews #sports #upset #shockingresult",
        "tags": ["premierleague", "epl", "football", "soccer", "matchanalysis", "highlights", "upset", "footballnews", "sports", "england"],
    },
    {
        "title": "Today's Football Roundup: EVERYTHING You Missed! \u26a1",
        "description": "Busy day? We've got you covered. Here's every goal, every card, every big moment from today's football action across all major leagues.\n\n\ud83d\udd14 SUBSCRIBE so you never miss a video!\n\ud83d\udc4d LIKE to help the channel grow!\n\ud83d\udcac COMMENT your team below!\n\n#footballnews #football #soccer #highlights #dailysports #sportsnews #premierleague #laliga #seriea #bundesliga #championsleague",
        "tags": ["footballnews", "football", "soccer", "highlights", "dailysports", "sportsnews", "premierleague", "laliga", "seriea", "bundesliga", "championsleague"],
    },
    {
        "title": "BREAKING: \ud83d\udd25 Major Transfer Confirmed \u2014 Here's What We Know",
        "description": "The transfer window is heating up! We break down the latest confirmed deal including fee, contract length, medical details, and what this means for both clubs.\n\n\ud83d\udd14 SUBSCRIBE for transfer news FIRST!\n\ud83d\udc4d LIKE to stay updated!\n\n#transfers #footballtransfernews #soccer #premierleague #laliga #transferwindow #footballnews #transferrumors #breakingnews",
        "tags": ["transfers", "footballtransfernews", "soccer", "premierleague", "laliga", "transferwindow", "transferrumors", "footballnews", "breakingnews"],
    },
    {
        "title": "UNBELIEVABLE Record Broken \u2014 History Made! \ud83c\udfc6",
        "description": "A historic moment in football just happened. We analyze the record-breaking performance, compare it to legends of the game, and explain why this is so special.\n\n\ud83d\udd14 SUBSCRIBE for more incredible content!\n\ud83d\udc4D DROP A LIKE for the record-breaker!\n\n#footballrecords #soccerstars #goals #highlights #premierleague #championsleague #football #history #recordbreaking",
        "tags": ["footballrecords", "soccerstars", "goals", "highlights", "premierleague", "championsleague", "football", "history", "recordbreaking", "sports"],
    },
    {
        "title": "DEEP DIVE: Match Analysis You Won't See on TV \ud83d\udcca",
        "description": "Professional tactical breakdown of the biggest match. Formations, pressing traps, counter-attacking patterns, and key individual battles \u2014 explained simply.\n\n\ud83d\udd14 SUBSCRIBE for expert analysis!\n\ud83d\udc4d LIKE if you learned something!\n\n#matchanalysis #footballhighlights #socceranalysis #premierleague #tactics #football #soccer #analysis #footballtactics",
        "tags": ["matchanalysis", "footballhighlights", "socceranalysis", "premierleague", "tactics", "football", "soccer", "analysis", "footballtactics"],
    },
    {
        "title": "Next SUPERSTAR? \u2b50 These Young Talents Are INCREDIBLE",
        "description": "The future of football is bright. We profile the most exciting young players in Europe right now \u2014 their stats, playing style, and potential.\n\n\ud83d\udd14 SUBSCRIBE to discover future stars!\n\ud83d\udc4d LIKE to support young talent!\n\n#youngtalents #risingstars #football #soccer #premierleague #laliga #seriea #bundesliga #futurestars #footballprodigy",
        "tags": ["youngtalents", "risingstars", "football", "soccer", "premierleague", "laliga", "seriea", "bundesliga", "futurestars", "footballprodigy"],
    },
    {
        "title": "Premier League WRAP: Every Goal & Talking Point \ud83c\udff4\udb40\udc67\udb40\udc62\udb40\udc65\udb40\udc6e\udb40\udc67\udb40\udc7f",
        "description": "Full Premier League roundup! All the goals, controversial decisions, fan reactions, and what it means for the table. Your one-stop EPL recap.\n\n\ud83d\udd14 SUBSCRIBE for PL content every week!\n\ud83d\udc4d LIKE for the Premier League!\n\n#premierleague #epl #footballhighlights #goals #soccer #england #football #premierleaguehighlights #matchday",
        "tags": ["premierleague", "epl", "footballhighlights", "goals", "soccer", "england", "football", "premierleaguehighlights", "matchday", "sports"],
    },
    {
        "title": "Champions League NIGHTS Are BACK! \ud83c\udfc6 Best Moments",
        "description": "The UEFA Champions League delivered another unforgettable night of football drama. We bring you every goal, save, and celebration from matchday.\n\n\ud83d\udd14 SUBSCRIBE for UCL content!\n\ud83d\udc4d LIKE for European nights!\n\n#championsleague #ucl #footballhighlights #goals #europe #soccer #football #uefachampionsleague #championsleaguehighlights",
        "tags": ["championsleague", "ucl", "footballhighlights", "goals", "europe", "soccer", "football", "uefachampionsleague", "championsleaguehighlights"],
    },
    {
        "title": "MIND-BLOWING Football Facts You Never Knew! \ud83e\udd2f",
        "description": "These incredible football statistics and stories will completely change how you see the beautiful game. Some of these are almost unbelievable!\n\n\ud83d\udd14 SUBSCRIBE for more amazing content!\n\ud83d\udc4d LIKE for football trivia!\n\n#footballfacts #soccerfacts #trivia #football #soccer #interestingfacts #didyouknow #footballtrivia #sportsfacts",
        "tags": ["footballfacts", "soccerfacts", "trivia", "football", "soccer", "interestingfacts", "didyouknow", "footballtrivia", "sportsfacts"],
    },
    {
        "title": "SACKED! \ud83d\udd25 Another Manager Leaves \u2014 What Went Wrong?",
        "description": "The managerial merry-go-round continues. We analyze why this manager lost his job, what went wrong tactically, and who could replace him.\n\n\ud83d\udd14 SUBSCRIBE for football news!\n\ud83d\udc4d LIKE if you agree with the decision!\n\n#footballmanagers #sackrace #premierleague #soccernews #footballnews #manager #sacking #coaching #tactics",
        "tags": ["footballmanagers", "sackrace", "premierleague", "soccernews", "footballnews", "manager", "sacking", "coaching", "tactics", "sports"],
    },
    {
        "title": "FANS WENT CRAZY! \ud83d\ude2e Best Stadium Moments This Week",
        "description": "The best atmosphere, tifos, celebrations, and fan moments from stadiums around the world. This is what makes football the beautiful game.\n\n\ud83d\udd14 SUBSCRIBE for fan culture content!\n\ud83d\udc4d LIKE if you love the atmosphere!\n\n#footballfans #stadiumatmosphere #soccer #football #fans #tifo #atmosphere #footballculture #ultras",
        "tags": ["footballfans", "stadiumatmosphere", "soccer", "football", "fans", "tifo", "atmosphere", "footballculture", "ultras"],
    },
    {
        "title": "Transfer Window: EVERY Deal Confirmed So Far \ud83d\udcdd",
        "description": "Complete transfer tracker with all confirmed deals, fees, contract details, and expert analysis on whether each signing is a bargain or overpriced.\n\n\ud83d\udd14 SUBSCRIBE for transfer updates!\n\ud83d\udc4d LIKE to support the channel!\n\n#transfers #transferwindow #footballnews #soccer #premierleague #laliga #seriea #bundesliga #transfernews #sports",
        "tags": ["transfers", "transferwindow", "footballnews", "soccer", "premierleague", "laliga", "seriea", "bundesliga", "transfernews", "sports"],
    },
    {
        "title": "The GREATEST Underdog Story in Football \ud83d\ude4c",
        "description": "This is the most inspiring football story you'll hear all year. How a team written off by everyone defied impossible odds to achieve greatness.\n\n\ud83d\udd14 SUBSCRIBE for incredible stories!\n\ud83d\udc4d LIKE to support underdogs!\n\n#underdog #footballstory #inspiration #soccer #football #comeback #sportsstory #inspiring #motivation",
        "tags": ["underdog", "footballstory", "inspiration", "soccer", "football", "comeback", "sportsstory", "inspiring", "motivation"],
    },
    {
        "title": "WORST MISSES of the Week! \ud83e\udd2f How Did They Miss?!",
        "description": "From open goals to penalty blunders \u2014 these shocking misses will have you laughing and crying at the same time. Worst finishing ever!\n\n\ud83d\udd14 SUBSCRIBE for more football fun!\n\ud83d\udc4d LIKE if you could have scored these!\n\n#funnyfootball #misses #soccerfails #footballfails #comedy #footballshorts #goals #funnymoments #sportscomedy",
        "tags": ["funnyfootball", "misses", "soccerfails", "footballfails", "comedy", "footballshorts", "goals", "funnymoments", "sportscomedy"],
    },
]


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
        body_parts.append("\n\u26bd Today's fixtures:")
        body_parts.append(match_text)

    if stories:
        body_parts.append("\n\ud83d\udcf0 Top football stories:")
        for i, s in enumerate(stories[:3], 1):
            body_parts.append(f"{i}. {s}")

    outros = [
        "\nWhat do you think about today's news? Drop your thoughts in the comments below! Don't forget to subscribe and hit that bell icon for daily football updates!",
        "\nWhich story caught your attention the most? Let us know in the comments! Subscribe now so you never miss another video!",
        "\nThanks for watching! If you enjoyed this update, smash that like button and subscribe for more football content every day!",
    ]

    body_parts.append(random.choice(outros))

    script = "\n\n".join(body_parts)
    return {
        "title": template["title"],
        "description": template["description"],
        "tags": template["tags"],
        "script": script,
    }
