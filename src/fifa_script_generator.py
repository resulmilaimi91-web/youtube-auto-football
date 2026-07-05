import random
from datetime import datetime
from src.trends_fetcher import get_trending_script_topic

TEMPLATES = [
    {
        "title": "Football Records That Will NEVER Be Broken!",
        "script": """Welcome back to Football Highlights Daily. Today is {date}, and we are looking at football records that will stand forever. These are the records that define the beautiful game.

Let us start with the goalscorers. Pele scored 1,279 goals in his career, a record that may never be beaten. Romario scored over 1,000 goals. Cristiano Ronaldo has scored over 900 career goals and counting. Lionel Messi has also passed 800 goals. These are numbers that most players can only dream of.

But it is not just about goals. The fastest goal in football history was scored by Nawaf Al-Abed in just 2.4 seconds. Yes, you read that correctly. 2.4 seconds. The goalkeeper had barely taken his position when the ball was already in the net.

The most red cards in football history belong to Gerardo Bedoya with 46 red cards. That is an entire career of discipline issues. Compare that to players like Andres Iniesta who never received a red card in his entire career.

The most expensive transfer in football history remains Neymar's move to PSG for 222 million euros. That transfer completely changed the market and prices have never been the same since.

The longest unbeaten streak in top-flight football belongs to Celtic with 62 games. AC Milan once went 58 games unbeaten in Serie A. Arsenal went 49 games unbeaten in the Premier League.

These are the records that make football the most beautiful sport in the world. Subscribe for more amazing football content every day!""",
    },
    {
        "title": "Top 10 Most Skilful Footballers Of All Time!",
        "script": """Hey there football fans, welcome back to Football Highlights Daily. It is {date}, and today we are counting down the most skilful footballers to ever play the game.

Number 10: Neymar Jr. The Brazilian magician with the most tricks in modern football. His creativity and flair make him one of the most entertaining players ever.

Number 9: Ronaldinho. The man who made football look like art. His no-look passes, elastico moves, and free kicks were absolutely legendary. He is the reason many of us fell in love with football.

Number 8: Cristiano Ronaldo. His step-overs, the chop, the knuckleball free kicks. His skill combined with his athleticism made him unstoppable for over a decade.

Number 7: Lionel Messi. The greatest dribbler in football history. His close control, balance, and ability to beat defenders in tight spaces is unmatched.

Number 6: Jay-Jay Okocha. The Nigerian legend who did things with a football that seemed impossible. He played with a smile and entertained millions.

Number 5: Zinedine Zidane. The elegance, the control, the 1998 World Cup final. His touch was like velvet and his vision was extraordinary.

Number 4: Diego Maradona. The 1986 World Cup was his stage. His dribbling through half of England is the most iconic goal in football history.

Number 3: Pele. The King of football. His skills, his goals, his three World Cup titles. He defined football for an entire generation.

Number 2: Johan Cruyff. The Cruyff turn changed football forever. His intelligence and technique were decades ahead of their time.

Number 1: Ronaldo Nazario. The original Ronaldo, before Cristiano and Messi. His pace, power, and skill at 19 years old was unbelievable. He is the most complete striker football has ever seen.

Which skilful player is your favourite? Comment below and subscribe for more daily football content!""",
    },
    {
        "title": "The Craziest Moments In Football History!",
        "script": """Welcome back to Football Highlights Daily. Today is {date}, and we are looking at the craziest moments in football history. These are the moments that left fans speechless.

The 2005 Champions League final. Liverpool were 3-0 down against AC Milan at halftime. What happened next is the greatest comeback in football history. Liverpool scored three goals in six minutes and went on to win on penalties.

The 2014 World Cup. Germany scored seven goals against Brazil. In Brazil. On Brazilian soil. The entire nation was in shock. It was the most one-sided semi-final in World Cup history.

Then there is the hand of God. Diego Maradona punched the ball into the net against England in the 1986 World Cup. He later said it was "the hand of God." Minutes later, he scored the goal of the century.

The craziest transfer story: Carlos Tevez and Javier Mascherano joined West Ham United in 2006 in a deal so complicated it led to court cases and a 5 million pound fine.

Remember when Eric Cantona kung-fu kicked a fan? Or when Zinedine Zidane headbutted Marco Materazzi in the World Cup final? These moments are part of football's rich and unpredictable history.

Football is never boring. Subscribe for more incredible football stories!""",
    },
]


def generate_script(match_text=None, all_stories=None):
    topic = get_trending_script_topic("fifa")
    template = random.choice(TEMPLATES)
    today = datetime.now().strftime("%B %d, %Y")

    script = template["script"].format(date=today)

    script += f"\n\nToday's hot topic: {topic}. What do you think about this? Let us know in the comments and subscribe for daily football content!"

    return {
        "title": template["title"],
        "script": script,
        "description": f"Amazing football highlights, records, and moments. Today's topic: {topic}\n\nAll footage and images are generated or stock. This content is for educational and entertainment purposes only. All statistics and information are based on publicly available data.\n\n#Football #Soccer #Highlights #Sports #FootballHistory",
        "tags": ["Football", "Soccer", "Highlights", "Sports", "FootballHistory", "Records", "Skills"],
        "category": "17",
    }
