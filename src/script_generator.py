import random
from datetime import datetime

TEMPLATES = [
    {
        "title": "FIFA WORLD CUP 2026: Everything You Need To Know!",
        "script": """Welcome back to Football Highlights Daily. Today is {date}, and we have got a packed show covering everything about the FIFA World Cup 2026.

Let us start with the basics. The 2026 World Cup will be hosted across three nations: the United States, Mexico, and Canada. This is the first time in history that three countries will co-host the tournament, and it promises to be absolutely massive.

The tournament kicks off on June 11th and runs through July 19th, 2026. That is 39 days of non-stop football action across 16 incredible host cities. From the iconic MetLife Stadium in New York to the legendary Estadio Azteca in Mexico City, every match will be played in world-class venues.

Now, here is where it gets really exciting. For the first time ever, the World Cup will feature 48 teams instead of the usual 32. That means more nations, more matches, and more drama. We are talking about 104 total matches, with teams from every corner of the globe competing for the most prestigious trophy in football.

The format has also changed. Teams will be divided into 12 groups of four, with the top two from each group advancing, along with the eight best third-placed teams. That gives us a brand new round of 32 knockout stage.

So, which team are you backing to win it all? Will it be defending champions Argentina, or will a new king be crowned? Drop your predictions in the comments below, and do not forget to subscribe for daily World Cup coverage.""",
    },
    {
        "title": "World Cup 2026: Host Cities And Stadiums Revealed!",
        "script": """Hello and welcome to Football Highlights Daily. It is {date}, and today we are taking you on a complete tour of all 16 host cities for the 2026 FIFA World Cup.

Starting in the United States, we have got eleven incredible cities. Atlanta will host matches at the Mercedes-Benz Stadium, home of the Atlanta Falcons. Boston brings us to Gillette Stadium, while Dallas will use the massive AT and T Stadium with its retractable roof.

Houston, Kansas City, Los Angeles, Miami, and Seattle all have stunning venues ready to welcome the world. And of course, the final will be held at MetLife Stadium in New Jersey, just outside New York City.

Moving up to Canada, Toronto will host matches at BMO Field, while Vancouver welcomes fans at BC Place. Both cities are ready to showcase Canadian football culture to the world.

In Mexico, we have three legendary venues. Mexico City's Estadio Azteca, which hosted the 1970 and 1986 World Cup finals, will once again be center stage. Guadalajara and Monterrey round out the Mexican venues with their modern stadiums.

Each city has been preparing for years to host this tournament. New infrastructure, upgraded stadiums, and world-class hospitality will make this the greatest World Cup ever.

Which host city are you most excited to visit? Let us know in the comments, and subscribe for more World Cup content!""",
    },
    {
        "title": "Top 10 Players To Watch At World Cup 2026!",
        "script": """Hey there football fans, welcome back to Football Highlights Daily. Today is {date}, and we are counting down the top 10 players who will light up the 2026 FIFA World Cup.

Number 10: Jude Bellingham. The English midfielder has been absolutely sensational at Real Madrid, and he will be leading England's charge in North America.

Number 9: Vinicius Junior. The Brazilian winger is pure electricity on the pitch. His pace and skill will terrorize defenses.

Number 8: Pedri. Spain's midfield maestro controls the tempo of every game he plays. At just 23, he will be in his prime.

Number 7: Bukayo Saka. Arsenal's star has become one of the most dangerous attackers in world football.

Number 6: Florian Wirtz. The German prodigy has taken the Bundesliga by storm and will be Germany's key man.

Number 5: Phil Foden. The Manchester City playmaker can unlock any defense with his vision and creativity.

Number 4: Kylian Mbappe. Already a World Cup winner, the French superstar will be looking to add another trophy to his collection.

Number 3: Erling Haaland. The Norwegian goal machine has broken every record at Manchester City.

Number 2: Lamine Yamal. The Spanish teenager is rewriting history books at Barcelona.

And number 1: Lionel Messi. Even at 39, if he plays, he remains the greatest of all time.

Who is your number one? Drop your list in the comments and subscribe for daily football content!""",
    },
    {
        "title": "World Cup 2026 Qualification: Who Has Made It?",
        "script": """Good morning football fans, welcome to Football Highlights Daily. It is {date}, and we have got the latest World Cup 2026 qualification updates for you.

The qualification process has been one of the most dramatic in World Cup history. Let us break down who has already booked their tickets to North America.

From Europe, powerhouses like France, England, Spain, Germany, and Italy have all qualified. The defending champions Argentina secured their spot from South America, along with Brazil, Uruguay, and Colombia.

In Asia, Japan, South Korea, Australia, and Iran have earned their places. Africa has sent five strong representatives including Morocco, who made history at the 2022 World Cup, along with Senegal, Tunisia, Cameroon, and Ghana.

From the CONCACAF region, hosts USA, Mexico, and Canada automatically qualified, while Costa Rica and Jamaica joined them through qualification.

That leaves us with some incredible teams still fighting for the remaining spots. Play-offs and final qualification rounds will determine the last few places.

The tournament will feature some首次 appearances too. Cape Verde, Curacao, Jordan, and Uzbekistan could all make their World Cup debuts.

Every four years, the World Cup brings the entire world together. And in 2026, with 48 teams competing, it will be bigger and better than ever.

Subscribe now so you do not miss any qualification updates!""",
    },
    {
        "title": "World Cup 2026: Prize Money And What Is At Stake!",
        "script": """Welcome back to Football Highlights Daily. Today is {date}, and we are diving into the massive prize money pool for the 2026 FIFA World Cup.

FIFA has announced a record-breaking prize fund for the 2026 tournament. The total purse has increased significantly from the 2022 World Cup in Qatar.

Every participating nation will receive a guaranteed participation fee just for qualifying. But the real money comes from performance. Teams that advance through the group stage will earn additional bonuses.

The further you go, the more you earn. Round of 16, quarter-finals, semi-finals, and of course, the final each come with increasing prize money.

The winning nation will take home a staggering amount, making it the richest prize in football history. Individual awards will also be given, including the Golden Boot for top scorer, the Golden Ball for best player, and the Golden Glove for best goalkeeper.

Beyond the prize money, there is something even more valuable at stake: legacy. Players dream of lifting that trophy since they were children. Nations unite behind their teams, and for one month, the whole world watches football.

The 2026 World Cup promises to be the biggest sporting event ever. With 48 teams, 104 matches, and billions of viewers, this is where legends are made.

Who do you think will lift the trophy? Comment below and subscribe for more World Cup content!""",
    },
]


def generate_script(match_text="", stories=None):
    template = random.choice(TEMPLATES)
    date_str = datetime.now().strftime("%B %d, %Y")

    script = template["script"].format(date=date_str)

    if match_text and "no matches" not in match_text.lower():
        parts = script.split("Subscribe")
        if len(parts) == 2:
            script = parts[0] + f"Before we go, here are the latest match results: {match_text} " + "Subscribe" + parts[1]

    tags = ["worldcup2026", "fifa", "worldcup", "football", "soccer", "footballnews", "sports"]
    extras = random.sample(["highlights", "footballhighlights", "worldcup2026", "fifaworldcup", "2026worldcup", "dailyfootball", "dailysoccer"], 5)
    tags.extend(extras)

    return {
        "title": template["title"],
        "description": f"""{script[:200]}...

SUBSCRIBE for daily World Cup 2026 coverage!
LIKE to support the channel!
COMMENT your predictions!

#worldcup2026 #fifa #football #soccer #worldcup #footballnews #highlights #sports #football2026 #fifaworldcup""",
        "tags": tags,
        "hashtags": ["worldcup2026", "fifa", "football", "soccer", "worldcup"],
        "script": script,
    }
