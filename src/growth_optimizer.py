import os
import random
import json
from datetime import datetime, timedelta


GOAL_WATCH_HOURS = 4000
GOAL_DAYS = 7
DAILY_HOURS_NEEDED = GOAL_WATCH_HOURS / GOAL_DAYS
MINUTES_PER_DAY = DAILY_HOURS_NEEDED * 60


def calculate_daily_target():
    return {
        "goal_watch_hours": GOAL_WATCH_HOURS,
        "days_left": GOAL_DAYS,
        "daily_hours_needed": round(DAILY_HOURS_NEEDED, 1),
        "daily_minutes_needed": round(MINUTES_PER_DAY, 0),
        "videos_per_day": 6,
        "avg_video_length_min": 12,
        "target_views_per_video": int(MINUTES_PER_DAY / 12 / 6),
    }


def get_optimized_script(topic="general", length="long"):
    templates = {
        "long": [
            {
                "title": "FIFA WORLD CUP 2026: The COMPLETE Preview Nobody Talks About!",
                "script": """Welcome back to Football Highlights Daily. Today is {date}, and this is the most comprehensive FIFA World Cup 2026 preview you will find anywhere on YouTube. Grab a coffee because we are going deep.

Let us start with the format. For the first time in World Cup history, 48 teams will compete across 16 venues in three countries. That is 104 matches over 39 days of non-stop football action.

The tournament kicks off on June 11th at Estadio Azteca in Mexico City, one of the most iconic stadiums in football history. The final will be held on July 19th at MetLife Stadium in New Jersey.

Now, let us break down the groups. The draw has created some fascinating matchups. We have got groups of death, underdog stories waiting to happen, and rivalries that will captivate the world.

From Europe, traditional powerhouses like France, England, Spain, and Germany have all qualified. But do not sleep on teams like the Netherlands, Portugal, and Belgium. They could surprise everyone.

South America brings us Argentina, the defending champions, led by what could be Lionel Messi's final World Cup. Brazil, Uruguay, and Colombia are all dangerous.

Africa has produced some incredible talent recently. Morocco made history at the 2022 World Cup, and they will be looking to go even further. Senegal, Cameroon, and Ghana are all capable of upsets.

Asia is represented by Japan, South Korea, Australia, and Iran. These teams have improved dramatically over the past decade.

From the host nations, the United States has a young, exciting squad. Mexico will have the crowd behind them. And Canada, with Alphonso Davies, could be the surprise package.

The key dates to mark in your calendar: the group stage runs from June 11th to June 27th. The round of 32 starts on June 29th. The round of 16 is on July 1st and 2nd. Quarter-finals on July 4th and 5th. Semi-finals on July 8th and 9th. And the big one, the final, on July 19th.

Who do I think will win? I am going with France. They have the squad depth, the experience, and Kylian Mbappe is on a mission. But Argentina will be desperate to defend their title, and you can never count out Brazil.

Drop your predictions in the comments. Who is your dark horse? Who will lift the trophy? Let me know. And if you found this preview helpful, smash that subscribe button because we will be covering every single match of this World Cup.

See you in the next video.""",
            },
            {
                "title": "World Cup 2026: Every Host City RANKED From Worst To Best!",
                "script": """Hey there football fans, welcome back to Football Highlights Daily. It is {date}, and today we are ranking all 16 host cities for the 2026 FIFA World Cup from worst to best. This is going to be controversial.

Starting at number 16, we have got Kansas City. Arrowhead Stadium is impressive, but Kansas City simply does not have the international appeal of other host cities. It is a football city, but not a global destination.

Number 15 is Philadelphia. Lincoln Financial Park is a solid venue, but Philadelphia overshadows it with its other sports teams. The World Cup will struggle to get attention here.

Number 14 goes to Atlanta. Mercedes-Benz Stadium is beautiful with its retractable roof, but Atlanta is more of an NFL city than a football city.

Number 13 is Seattle. Lumen Field will be electric with the Sounders fans, but Seattle is geographically isolated from other host cities.

Number 12 is Vancouver. BC Place is a great venue, but Canada only has two host cities, which limits the atmosphere.

Number 11 is Monterrey. Estadio BBVA is stunning, but Monterrey often gets overshadowed by Mexico City.

Number 10 is Guadalajara. Estadio Akron is modern and the city has incredible culture, but it lacks the star power of bigger venues.

Number 9 is Boston. Gillette Stadium is iconic, but it is located outside the city center which reduces the fan experience.

Number 8 is Houston. NRG Stadium is massive and the city has a huge Hispanic population that will create an amazing atmosphere.

Number 7 is Dallas. AT and T Stadium is a fortress and Jerry World will put on a show, but the Texas heat in summer could be brutal.

Number 6 is Toronto. BMO Field is intimate and the city is incredibly diverse, making it a perfect World Cup host.

Number 5 is Mexico City. Estadio Azteca is legendary, having hosted two World Cup finals. The altitude and atmosphere make it one of the most intimidating venues in world football.

Number 4 is Los Angeles. SoFi Stadium is the most expensive stadium ever built and it will host some incredible matches.

Number 3 is Seattle. Wait, I already ranked Seattle. Let me fix that. Number 3 is Miami. Hard Rock Stadium will be the place to be with its beach culture and party atmosphere.

Number 2 is New York. MetLife Stadium will host the final and there is no bigger stage in world football.

And number 1, the best host city for the 2026 World Cup is Mexico City. The passion, the history, the atmosphere. Estadio Azteca is cathedral of football and it will be absolutely electric.

What do you think? Did I get the ranking right? Let me know in the comments and subscribe for more World Cup content!""",
            },
            {
                "title": "10 INSANE Facts About World Cup 2026 Nobody Knows!",
                "script": """What is going on football fans, welcome back to Football Highlights Daily. It is {date}, and today I am going to blow your mind with 10 insane facts about the 2026 FIFA World Cup that almost nobody knows about.

Fact number 10: The 2026 World Cup will be the most expensive sporting event in history. The combined investment from all three host nations exceeds 5 billion dollars. That is more than the last three World Cups combined.

Fact number 9: There will be more matches at the 2026 World Cup than at any previous tournament. 104 matches compared to 64 at the 2022 World Cup. That is 40 extra matches of pure football drama.

Fact number 8: The time zones work perfectly for global TV audiences. Matches will be played across three time zones, meaning fans in Europe, Asia, and the Americas can all watch live at reasonable hours.

Fact number 7: The United States will host matches in 11 different cities, more than any other country in World Cup history. Previously, Mexico held the record with 12 cities in 1970 and 1986.

Fact number 6: The final at MetLife Stadium will have a capacity of over 82,000 fans. That makes it one of the largest World Cup final venues ever.

Fact number 5: For the first time, the World Cup will use semi-automated offside technology in every single match. This means faster and more accurate offside decisions.

Fact number 4: The prize money pool for 2026 is expected to exceed 1 billion dollars. The winning team will take home approximately 60 million dollars.

Fact number 3: Mexico will become the first country to host the men's World Cup three times. They hosted in 1970 and 1986, and now they co-host in 2026.

Fact number 2: The tournament will feature 48 teams for the first time ever. That is 16 more teams than any previous World Cup, giving more nations a chance to compete on the biggest stage.

And fact number 1: If you add up the total distance all teams will travel during the tournament, it exceeds 100,000 kilometers. That is more than twice the circumference of the Earth.

Which fact surprised you the most? Drop a comment below and subscribe for daily World Cup content. See you in the next video!""",
            },
            {
                "title": "World Cup 2026: The Teams Nobody Is Talking About But Should!",
                "script": """Hello everyone, welcome back to Football Highlights Daily. Today is {date}, and we are talking about the dark horses of the 2026 FIFA World Cup. These are the teams that nobody is paying attention to, but they could shock the world.

First up, Morocco. Yes, they made the semi-finals in 2022, but people seem to have forgotten how good they are. They have got Achraf Hakimi, Noussair Mazraoui, and a defensive structure that is incredibly difficult to break down. Do not be surprised if they go deep again.

Next, Japan. The Blue Samurai have been quietly building one of the most exciting squads in world football. With players like Takefusa Kubo, Kaoru Mitoma, and Takumi Minamino, they have got the skill and the speed to beat anyone on their day.

South Korea is another team to watch. Son Heung-min is still world-class, and the next generation of Korean talent is emerging. They have got a point to prove after a disappointing 2022 campaign.

Senegal are always dangerous. They have got Sadio Mane, Kalidou Koulibaly, and a team full of Premier League experience. African teams always bring passion and energy that can upset the bigger nations.

Canada might be the ultimate dark horse. With Alphonso Davies leading the charge and a young, hungry squad, they could be the surprise package of the tournament. Playing at home gives them a massive advantage.

Australia always overperform at World Cups. They might not have the biggest names, but they play as a team and they never give up. They are incredibly difficult to beat.

Ecuador have got some seriously talented players. Moises Caicedo is one of the best midfielders in the Premier League, and they have got a strong defensive core.

Serbia always produce talented footballers. With Dusan Vlahovic, Aleksandar Mitrovic, and a creative midfield, they can score goals against anyone.

Uruguay might be getting older, but they have still got Edinson Cavani and Luis Suarez, plus emerging talents like Federico Valverde. They are always competitive at World Cups.

And finally, Wales. If Gareth Bale comes out of retirement for one last World Cup, Wales could be incredibly dangerous. They have got a passionate fanbase and a team that believes.

Who is your dark horse for the 2026 World Cup? Let me know in the comments and subscribe for more World Cup content!""",
            },
            {
                "title": "How To Watch EVERY World Cup 2026 Match For FREE!",
                "script": """Hey football fans, welcome back to Football Highlights Daily. It is {date}, and today I am going to show you how to watch every single match of the 2026 FIFA World Cup for free. Yes, you heard that right. Every match, completely free.

In the United States, Fox Sports has the broadcasting rights, but you can watch for free on Tubi, which is Fox's free streaming service. Just download the app and you are good to go.

In the United Kingdom, the BBC and ITV share the rights. BBC iPlayer and ITV Hub will both stream matches for free. You just need a TV license, which most people already have.

In Canada, CTV and TSN have the rights, but you can watch on CTV's website and app for free with a Canadian IP address.

In Australia, SBS has the rights and they stream every match for free on SBS On Demand.

If you are in a country without free coverage, there are other options. FIFA itself will stream some matches on their YouTube channel for free. Not all matches, but a good selection.

Another option is to use a VPN. Services like NordVPN or ExpressVPN can help you access free streaming services from other countries. Just connect to a server in the UK or Australia and use their free streaming services.

Social media is another great option. FIFA posts highlights, goals, and key moments on their social media channels throughout the tournament. YouTube, Twitter, Instagram, and TikTok will all have content.

Local sports bars and restaurants often show World Cup matches for free. You just need to buy a drink or some food and you can watch the game with other fans.

FIFA fan zones are set up in host cities and around the world. These are free public viewing areas with giant screens and an incredible atmosphere.

And of course, you can always listen to live commentary on the radio. BBC Radio 5 Live and other radio stations provide free commentary of every match.

So there you have it. Multiple ways to watch the entire 2026 FIFA World Cup for free. No excuses to miss a single goal.

Which method will you use? Let me know in the comments and subscribe for more World Cup content!""",
            },
        ],
    }

    length_templates = templates.get(length, templates["long"])
    template = random.choice(length_templates)
    date_str = datetime.now().strftime("%B %d, %Y")
    script = template["script"].format(date=date_str)

    return {
        "title": template["title"],
        "description": f"""{script[:200]}...

SUBSCRIBE for daily World Cup 2026 coverage!
LIKE to support the channel!
COMMENT your predictions!

#worldcup2026 #fifa #football #soccer #worldcup #footballnews #highlights #sports #football2026 #fifaworldcup""",
        "tags": ["worldcup2026", "fifa", "worldcup", "football", "soccer", "footballnews", "sports", "highlights", "worldcup2026", "fifaworldcup"],
        "hashtags": ["worldcup2026", "fifa", "football", "soccer", "worldcup"],
        "script": script,
    }


def get_video_config():
    return {
        "video_length_seconds": 720,
        "posting_interval_hours": 4,
        "videos_per_day": 6,
        "target_watch_minutes_per_video": 8,
        "thumbnail_style": "clickbait",
        "title_style": "caps_numbers_emotional",
    }


def track_progress(current_watch_hours, current_subscribers):
    target = calculate_daily_target()
    progress = {
        "current_watch_hours": current_watch_hours,
        "target_watch_hours": GOAL_WATCH_HOURS,
        "progress_percent": round((current_watch_hours / GOAL_WATCH_HOURS) * 100, 1),
        "hours_needed": round(GOAL_WATCH_HOURS - current_watch_hours, 1),
        "current_subscribers": current_subscribers,
        "subscribers_needed": max(0, 1000 - current_subscribers),
        "daily_target": target,
    }

    if current_watch_hours < GOAL_WATCH_HOURS * 0.3:
        progress["status"] = "NEEDS ACCELERATION"
        progress["action"] = "Increase posting frequency, create longer videos, focus on Shorts"
    elif current_watch_hours < GOAL_WATCH_HOURS * 0.7:
        progress["status"] = "ON TRACK"
        progress["action"] = "Maintain current strategy, optimize top-performing content"
    else:
        progress["status"] = "AHEAD OF SCHEDULE"
        progress["action"] = "Keep going, focus on quality over quantity"

    return progress


if __name__ == "__main__":
    target = calculate_daily_target()
    print(f"Goal: {target['goal_watch_hours']} watch hours in {target['days_left']} days")
    print(f"Daily target: {target['daily_hours_needed']} hours ({target['daily_minutes_needed']} minutes)")
    print(f"Videos per day: {target['videos_per_day']}")
    print(f"Avg video length: {target['avg_video_length_min']} minutes")
    print(f"Target views per video: {target['target_views_per_video']}")

    progress = track_progress(0, 0)
    print(f"\nProgress: {progress['progress_percent']}%")
    print(f"Status: {progress['status']}")
    print(f"Action: {progress['action']}")
