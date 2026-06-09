import random
from datetime import datetime

TEMPLATES = [
    {
        "title": "FIFA WORLD CUP 2026: The COMPLETE Guide Nobody Talks About!",
        "script": """Welcome back to Football Highlights Daily. Today is {date}, and this is the most comprehensive FIFA World Cup 2026 guide you will find anywhere on YouTube. We are going deep today, so grab a coffee and settle in because we have got a lot to cover.

Let us start with the basics. The 2026 World Cup will be hosted across three nations: the United States, Mexico, and Canada. This is the first time in World Cup history that three countries will co-host the tournament. The United States previously hosted in 1994, Mexico hosted in 1970 and 1986, and this will be Canada's first time hosting any World Cup.

The tournament kicks off on June 11th, 2026, at the legendary Estadio Azteca in Mexico City. This stadium has hosted two World Cup finals already, 1970 and 1986, and it will once again be the center of the football world. The final will be held on July 19th at MetLife Stadium in New Jersey, just outside New York City. That is 39 days of non-stop football action across 16 incredible host cities.

Now, here is where it gets really exciting. For the first time ever, the World Cup will feature 48 teams instead of the usual 32. That is 16 more teams than any previous World Cup. We are talking about 104 total matches, with teams from every corner of the globe competing for the most prestigious trophy in football.

The format has also changed significantly. Teams will be divided into 12 groups of four. The top two teams from each group will advance automatically. In addition, the eight best third-placed teams will also qualify for the knockout rounds. That gives us a brand new round of 32, which has never existed before in World Cup history.

From the round of 32 onwards, it is single elimination. The round of 32 starts on June 29th. The round of 16 takes place on July 1st and 2nd. Quarter-finals are on July 4th and 5th. Semi-finals on July 8th and 9th. The third-place match on July 18th. And the big one, the final, on July 19th.

Let us talk about the host cities in detail. In the United States, we have eleven cities. Atlanta will host at Mercedes-Benz Stadium, which has a retractable roof. Boston will use Gillette Stadium. Dallas will host at AT&T Stadium, the home of the Dallas Cowboys. Houston will use NRG Stadium. Kansas City will host at Arrowhead Stadium. Los Angeles will use the brand new SoFi Stadium. Miami will host at Hard Rock Stadium. New York and New Jersey will host the final at MetLife Stadium. Philadelphia will use Lincoln Financial Field. San Francisco Bay Area will host at Levi's Stadium. And Seattle will use Lumen Field.

In Mexico, we have three cities. Mexico City will use Estadio Azteca. Guadalajara will use Estadio Akron. And Monterrey will use Estadio BBVA.

In Canada, we have two cities. Toronto will host at BMO Field. And Vancouver will use BC Place.

Each of these venues has been preparing for years. New infrastructure, upgraded stadiums, and world-class hospitality will make this the greatest World Cup ever.

The qualification process has been one of the most dramatic in World Cup history. From Europe, powerhouses like France, England, Spain, Germany, and Italy have all qualified. Argentina, the defending champions, secured their spot from South America, along with Brazil, Uruguay, and Colombia.

From Asia, Japan, South Korea, Australia, and Iran have earned their places. Africa has sent five strong representatives including Morocco, who made history at the 2022 World Cup, along with Senegal, Tunisia, Cameroon, and Ghana.

Some首次 appearances too. Cape Verde, Curacao, Jordan, and Uzbekistan could all make their World Cup debuts.

So, which team are you backing to win it all? Will it be defending champions Argentina with Messi potentially playing his final World Cup? Will it be France with Kylian Mbappe on a mission? Will England finally end their wait? Will Brazil reclaim their throne? Or will a dark horse shock the world?

Drop your predictions in the comments below, and do not forget to subscribe for daily World Cup coverage. We will be covering every single match of this tournament.""",
    },
    {
        "title": "World Cup 2026: Every Host City RANKED From Worst To Best!",
        "script": """Hey there football fans, welcome back to Football Highlights Daily. It is {date}, and today we are ranking all 16 host cities for the 2026 FIFA World Cup from worst to best. This is going to be controversial, so buckle up.

Starting at number 16, we have got Kansas City. Arrowhead Stadium is impressive with its capacity of over 76,000, but Kansas City simply does not have the international appeal of other host cities. It is a great American football city, but for a global event like the World Cup, it lacks the infrastructure and tourism draw of bigger cities.

Number 15 is Philadelphia. Lincoln Financial Park is a solid venue that regularly hosts NFL games, but Philadelphia often gets overshadowed by New York just a short drive away. The World Cup will struggle to get attention here when New York is hosting the final.

Number 14 goes to Atlanta. Mercedes-Benz Stadium is beautiful with its retractable roof and modern design, but Atlanta is more of an NFL and NBA city than a football city. The local fanbase is growing but it is not yet a football hotbed.

Number 13 is Seattle. Lumen Field will be electric with the Sounders fans who are some of the most passionate in MLS, but Seattle is geographically isolated from other host cities on the West Coast.

Number 12 is Vancouver. BC Place is a great venue with its retractable roof, but Canada only has two host cities which limits the overall atmosphere and fan experience across the country.

Number 11 is Monterrey. Estadio BBVA is a stunning modern stadium, but Monterrey often gets overshadowed by Mexico City which has more history and prestige.

Number 10 is Guadalajara. Estadio Akron is modern and the city has incredible culture, food, and atmosphere, but it lacks the star power of bigger venues.

Number 9 is Boston. Gillette Stadium is iconic and has hosted many big events, but it is located about an hour outside the city center in Foxborough which reduces the fan experience significantly.

Number 8 is Houston. NRG Stadium is massive and the city has a huge Hispanic population that will create an incredible atmosphere for World Cup matches.

Number 7 is Dallas. AT&T Stadium is a fortress and Jerry World will put on an absolute show with its massive video board and luxury facilities. However, the Texas heat in summer could be brutal for players and fans.

Number 6 is Toronto. BMO Field is intimate and the city is incredibly diverse with populations from every football-loving nation. This will create an amazing multicultural atmosphere.

Number 5 is Mexico City. Estadio Azteca is legendary, having hosted two World Cup finals. The altitude at 2,240 meters above sea level and the passionate Mexican fans make it one of the most intimidating venues in world football.

Number 4 is Los Angeles. SoFi Stadium is the most expensive stadium ever built at 5.5 billion dollars and it will host some incredible matches in a city that loves football.

Number 3 is Miami. Hard Rock Stadium will be the place to be with its beach culture, party atmosphere, and large Latin American community that lives and breathes football.

Number 2 is New York. MetLife Stadium will host the final and there is no bigger stage in world football. 82,000 fans in the biggest media market on the planet.

And number 1, the best host city for the 2026 World Cup is Mexico City. The passion, the history, the atmosphere. Estadio Azteca is the cathedral of football and it will be absolutely electric for this tournament.

What do you think? Did I get the ranking right? Let me know in the comments and subscribe for more World Cup content!""",
    },
    {
        "title": "World Cup 2026: Top 20 Players You MUST Watch!",
        "script": """What is going on football fans, welcome back to Football Highlights Daily. It is {date}, and today we are counting down the top 20 players you absolutely must watch at the 2026 FIFA World Cup. This is going to be controversial.

Starting at number 20, Florian Wirtz. The German midfielder has been absolutely sensational at Bayer Leverkusen, helping them go unbeaten in the Bundesliga. At just 23, he will be Germany's key creative force and could be the breakout star of the tournament.

Number 19, Bukayo Saka. Arsenal's star has become one of the most dangerous attackers in the Premier League. His pace, skill, and finishing make him a constant threat on the right wing. England will rely on his creativity.

Number 18, Pedri. Spain's midfield maestro controls the tempo of every game he plays. He is the heartbeat of the Spanish team and at just 23, he is already one of the best midfielders in the world.

Number 17, Joao Felix. The Portuguese forward has found his form at Barcelona after years of inconsistency. His creativity and finishing make him a constant threat and Portugal will need him at his best.

Number 16, Federico Valverde. The Uruguayan midfielder is a box-to-box machine who can defend, pass, and score goals from anywhere on the pitch. He is the engine that drives Uruguay forward.

Number 15, Jamal Musiala. Bayern Munich's star is one of the most exciting young players in world football. His dribbling is mesmerizing and he can create goals out of nothing.

Number 14, Lautaro Martinez. Inter Milan's striker has been scoring goals for fun in Serie A. Argentina will rely on his finishing to complement Messi's creativity.

Number 13, Phil Foden. Manchester City's playmaker can unlock any defense with his vision and creativity. He has been incredible under Pep Guardiola and will be key for England.

Number 12, Vinicius Junior. The Brazilian winger is pure electricity on the pitch. His pace will terrorize defenders and he has the ability to change games in an instant.

Number 11, Rodri. Manchester City's midfield anchor is the best defensive midfielder in the world. He provides the foundation that allows City's attackers to flourish.

Number 10, Jude Bellingham. Real Madrid's star has been absolutely incredible since his move from Dortmund. England's talisman will be on a mission to bring football home.

Number 9, Erling Haaland. The Norwegian goal machine has broken every record at Manchester City. His finishing is lethal and he will be looking to lead Norway to a historic World Cup.

Number 8, Kevin De Bruyne. Even at 35, the Belgian maestro is still the best passer in world football. His vision and range of passing are unmatched.

Number 7, Kylian Mbappe. The French superstar will be looking to add another World Cup to his collection. He is arguably the best player in the world right now.

Number 6, Lamine Yamal. The Spanish teenager is rewriting history at Barcelona. At just 18, he could be the youngest World Cup winner ever.

Number 5, Mohamed Salah. The Egyptian king is still one of the best players in the world. His speed, skill, and finishing make him a constant threat.

Number 4, Harry Kane. Bayern Munich's striker has been scoring goals for fun. England's captain will lead the charge and is desperate to win a major trophy.

Number 3, Neymar. If fit, the Brazilian magician can still produce moments of pure genius. This could be his last World Cup and he will want to go out on top.

Number 2, Lionel Messi. Even at 39, he remains the greatest of all time. This could be his final World Cup and the world will be watching every touch.

And number 1, the player you absolutely must watch at World Cup 2026 is Kylian Mbappe. He will be the star of the tournament. His speed, skill, and finishing make him unstoppable. France are the favorites and Mbappe will be the reason why.

Who is your must-watch player? Let me know in the comments and subscribe for daily World Cup content!""",
    },
    {
        "title": "World Cup 2026: The Dark Horses Nobody Is Talking About!",
        "script": """Hello everyone, welcome back to Football Highlights Daily. Today is {date}, and we are talking about the dark horses of the 2026 FIFA World Cup. These are the teams that nobody is paying attention to, but they could shock the world.

First up, Morocco. Yes, they made the semi-finals in 2022 and shocked the world, but people seem to have forgotten how good they are. They have got Achraf Hakimi from PSG, Noussair Mazraoui from Manchester United, and a defensive structure that is incredibly difficult to break down. Their manager Walid Regragui has built a team that is greater than the sum of its parts. Do not be surprised if they go deep again.

Next, Japan. The Blue Samurai have been quietly building one of the most exciting squads in world football. With players like Takefusa Kubo from Real Sociedad, Kaoru Mitoma from Brighton, and Takumi Minamino, they have got the skill and the speed to beat anyone on their day. Japan has consistently improved at every World Cup and 2026 could be their best performance yet.

South Korea is another team to watch. Son Heung-min from Tottenham is still world-class and the next generation of Korean talent is emerging. They have got a point to prove after a disappointing 2022 campaign where they exited in the group stages. The hunger and determination of this Korean team could take them far.

Senegal are always dangerous in African football. They have got Sadio Mane, Kalidou Koulibaly, and a team full of Premier League experience. African teams always bring passion and energy that can upset the bigger nations. Senegal has the quality to beat anyone on their day.

Canada might be the ultimate dark horse. With Alphonso Davies from Bayern Munich leading the charge and a young, hungry squad, they could be the surprise package of the tournament. Playing at home in Toronto and Vancouver gives them a massive advantage. The Canadian football revolution is real and 2026 could be their moment.

Australia always overperform at World Cups. They might not have the biggest names, but they play as a team and they never give up. They are incredibly difficult to beat and have a never-say-die attitude that makes them dangerous opponents for anyone.

Ecuador have got some seriously talented players. Moises Caicedo from Chelsea is one of the best midfielders in the Premier League, and they have got a strong defensive core. South American football is always competitive and Ecuador could surprise a few teams.

Serbia always produce talented footballers. With Dusan Vlahovic from Juventus, Aleksandar Mitrovic, and a creative midfield, they can score goals against anyone. Serbian football is on the rise and they could make a deep run.

Uruguay might be getting older, but they have still got Edinson Cavani and Luis Suarez, plus emerging talents like Federico Valverde from Real Madrid. They are always competitive at World Cups and have the experience to go far.

And finally, Wales. If Gareth Bale comes out of retirement for one last World Cup, Wales could be incredibly dangerous. They have got a passionate fanbase and a team that believes they can compete with anyone.

These dark horses could be the story of the tournament. Who is your dark horse for the 2026 World Cup? Let me know in the comments and subscribe for more World Cup content!""",
    },
    {
        "title": "World Cup 2026: How To Watch EVERY Match For FREE!",
        "script": """Hey football fans, welcome back to Football Highlights Daily. It is {date}, and today I am going to show you how to watch every single match of the 2026 FIFA World Cup for free. Yes, you heard that right. Every match, completely free.

In the United States, Fox Sports has the broadcasting rights for the 2026 World Cup. But here is the thing, you can watch for free on Tubi, which is Fox's free streaming service. Just download the Tubi app on your phone, tablet, or smart TV, create a free account, and you are good to go. No subscription required. Every match will be available for free on Tubi.

In the United Kingdom, the BBC and ITV share the broadcasting rights. BBC iPlayer and ITV Hub will both stream matches for free. You just need a TV license, which most people in the UK already have. Both services are completely free and will show every match.

In Canada, CTV and TSN have the rights, but you can watch on CTV's website and app for free with a Canadian IP address. TSN requires a subscription but CTV is free.

In Australia, SBS has the rights and they stream every match for free on SBS On Demand. Just download the app or visit their website and you can watch for free.

If you are in a country without free coverage, there are other options. FIFA itself will stream some matches on their YouTube channel for free. Not all matches, but a good selection of group stage matches will be available on YouTube.

Another option is to use a VPN. Services like NordVPN or ExpressVPN can help you access free streaming services from other countries. Just connect to a server in the UK or Australia and use their free streaming services. This is completely legal and many people use this method.

Social media is another great option. FIFA posts highlights, goals, and key moments on their social media channels throughout the tournament. YouTube, Twitter, Instagram, and TikTok will all have content updated in real-time.

Local sports bars and restaurants often show World Cup matches for free. You just need to buy a drink or some food and you can watch the game with other fans in an incredible atmosphere.

FIFA fan zones are set up in host cities and around the world. These are free public viewing areas with giant screens and an incredible atmosphere. They are usually located in city centers and parks.

And of course, you can always listen to live commentary on the radio. BBC Radio 5 Live and other radio stations provide free commentary of every match.

So there you have it. Multiple ways to watch the entire 2026 FIFA World Cup for free. No excuses to miss a single goal.

Which method will you use? Let me know in the comments and subscribe for more World Cup content!""",
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
