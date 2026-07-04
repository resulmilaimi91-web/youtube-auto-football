import random
from datetime import datetime
from src.trends_fetcher import get_trending_script_topic

TEMPLATES = [
    {
        "title": "FIFA WORLD CUP 2026: The COMPLETE Guide Nobody Talks About!",
        "script": """Welcome back to Football Highlights Daily. Today is {date}, and this is the most comprehensive FIFA World Cup 2026 guide you will find anywhere on YouTube. We are going deep today, so grab a coffee and settle in because we have got a lot to cover.

Let us start with the basics. The 2026 World Cup will be hosted across three nations: the United States, Mexico, and Canada. This is the first time in World Cup history that three countries will co-host the tournament. The United States previously hosted in 1994, Mexico hosted in 1970 and 1986, and this will be Canada's first time hosting any World Cup.

The tournament kicks off on June 11th, 2026, at the legendary Estadio Azteca in Mexico City. This stadium has hosted two World Cup finals already, 1970 and 1986, and it will once again be the center of the football world. The final will be held on July 19th at MetLife Stadium in New Jersey, just outside New York City. That is 39 days of non-stop football action across 16 incredible host cities.

Now, here is where it gets really exciting. For the first time ever, the World Cup will feature 48 teams instead of the usual 32. That is 16 more teams than any previous World Cup. We are talking about 104 total matches, with teams from every corner of the globe competing for the most prestigious trophy in football.

The format has also changed significantly. Teams will be divided into 12 groups of four. The top two teams from each group will advance automatically. In addition, the eight best third-placed teams will also qualify for the knockout rounds. That gives us a brand new round of 32, which has never existed before in World Cup history.

From the round of 32 onwards, it is single elimination. The round of 32 starts on June 29th. The round of 16 takes place on July 1st and 2nd. Quarter-finals are on July 4th and 5th. Semi-finals on July 8th and 9th. The third-place match on July 18th. And the big one, the final, on July 19th.

So, which team are you backing to win it all? Will it be defending champions Argentina with Messi potentially playing his final World Cup? Will it be France with Kylian Mbappe on a mission? Will England finally end their wait? Will Brazil reclaim their throne? Or will a dark horse shock the world?

Drop your predictions in the comments below, and do not forget to subscribe for daily World Cup coverage. We will be covering every single match of this tournament.""",
    },
    {
        "title": "World Cup 2026: Every Host City RANKED From Worst To Best!",
        "script": """Hey there football fans, welcome back to Football Highlights Daily. It is {date}, and today we are ranking all 16 host cities for the 2026 FIFA World Cup from worst to best. This is going to be controversial, so buckle up.

The United States leads the way with eleven host cities. Atlanta, Boston, Dallas, Houston, Kansas City, Los Angeles, Miami, New York/New Jersey, Philadelphia, San Francisco Bay Area, and Seattle. Each city brings something unique to the tournament. Mexico contributes three historic venues: Mexico City's legendary Estadio Azteca, Guadalajara's Estadio Akron, and Monterrey's Estadio BBVA. Canada rounds out the list with Toronto's BMO Field and Vancouver's BC Place.

Let us start from the bottom. Every host city has prepared years for this moment. New infrastructure, upgraded stadiums, world-class hospitality. The United States last hosted in 1994 when the World Cup averaged nearly 69,000 fans per game - a record that still stands today. This time around, with modern stadiums and better infrastructure, those numbers could be shattered.

The most anticipated venues include SoFi Stadium in Los Angeles, AT&T Stadium in Dallas, and the final venue, MetLife Stadium in New Jersey. But dark horses like Arrowhead Stadium in Kansas City and Lumen Field in Seattle could create incredible atmospheres.

Which host city are you most excited about? Let me know in the comments!""",
    },
]


def generate_script(match_text=None, all_stories=None):
    topic = get_trending_script_topic("fifa")
    template = random.choice(TEMPLATES)
    today = datetime.now().strftime("%B %d, %Y")

    if match_text:
        match_section = f"\n\nNow let us look at what is happening in the football world today. {match_text}"
    else:
        match_section = ""

    if all_stories:
        news_section = f"\n\nIn other news, {random.choice(all_stories)}"
    else:
        news_section = ""

    script = template["script"].format(date=today)
    if match_section and len(script) + len(match_section) < 4000:
        script += match_section
    if news_section and len(script) + len(news_section) < 4000:
        script += news_section

    script += f"\n\nToday's trending topic: {topic}. Make sure to subscribe for more daily football content!"

    return {
        "title": template["title"],
        "script": script,
        "description": f"Full FIFA World Cup 2026 analysis and football highlights. Today's topic: {topic}\n\n#WorldCup2026 #FIFA #Football #Soccer #Highlights",
        "tags": ["WorldCup2026", "FIFA", "Football", "Soccer", "Highlights", "WorldCup"],
        "category": "17",
    }
