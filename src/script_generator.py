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
    {
        "title": "This Player Just Broke a HUGE Record! 🏆",
        "description": "Incredible individual performances and historic records shattered in today's matches. You won't believe what happened!",
        "tags": ["footballrecords", "soccerstars", "goals", "highlights", "premierleague", "championsleague", "football"],
    },
    {
        "title": "Match of the Week: Full Analysis & Highlights 📊",
        "description": "Deep dive into the biggest match of the week with expert analysis, key moments, and tactical breakdown.",
        "tags": ["matchanalysis", "footballhighlights", "socceranalysis", "premierleague", "tactics", "football"],
    },
    {
        "title": "Rising Stars: Young Players Taking Over Football ⭐",
        "description": "The next generation of football superstars is here. Discover the young talents making waves across Europe's top leagues.",
        "tags": ["youngtalents", "risingstars", "football", "soccer", "premierleague", "laliga", "seriea", "bundesliga"],
    },
    {
        "title": "Premier League Weekend Roundup 🇬🇧",
        "description": "All the goals, drama, and talking points from another action-packed Premier League weekend. Full roundup inside!",
        "tags": ["premierleague", "epl", "footballhighlights", "goals", "soccer", "england", "football"],
    },
    {
        "title": "Champions League: Best Moments This Week 🏅",
        "description": "The UEFA Champions League delivered another night of magic. Watch the best goals, saves, and celebrations from matchday.",
        "tags": ["championsleague", "ucl", "footballhighlights", "goals", "europe", "soccer", "football"],
    },
    {
        "title": "5 Football Facts You Probably Didn't Know 🤯",
        "description": "Mind-blowing football statistics and stories that will change how you see the beautiful game. Number 3 is unbelievable!",
        "tags": ["footballfacts", "soccerfacts", "trivia", "football", "soccer", "interestingfacts", "didyouknow"],
    },
    {
        "title": "Manager Sack Race: Who's Next to Go? 🔄",
        "description": "Pressure is mounting across Europe. We analyze which managers are on thin ice and who might be the next to leave.",
        "tags": ["footballmanagers", "sackrace", "premierleague", "soccernews", "footballnews", "manager"],
    },
    {
        "title": "Stadium Atmosphere: Best Fan Moments of the Week 📣",
        "description": "Football without fans is nothing. Relive the best crowd moments, tifos, and celebrations from stadiums around the world.",
        "tags": ["footballfans", "stadiumatmosphere", "soccer", "football", "fans", "tifo", "atmosphere"],
    },
    {
        "title": "Transfer Window: Every Confirmed Deal So Far 📝",
        "description": "Complete guide to every confirmed transfer with fees, contract lengths, and expert analysis on each signing.",
        "tags": ["transfers", "transferwindow", "footballnews", "soccer", "premierleague", "laliga", "seriea", "bundesliga"],
    },
    {
        "title": "Underdog Story of the Season That Has Everyone Talking 🐕",
        "description": "The most inspiring football story you'll hear today. How this underdog team defied all odds to achieve the impossible.",
        "tags": ["underdog", "footballstory", "inspiration", "soccer", "football", "comeback", "sportsstory"],
    },
    {
        "title": "Worst Misses of the Week (You Won't Believe These!) 😱",
        "description": "From open goals to point-blank range — these shocking misses will make you cringe. How did they not score?!",
        "tags": ["funnyfootball", "misses", "soccerfails", "footballfails", "comedy", "footballshorts", "goals"],
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
