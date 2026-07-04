import random
from datetime import datetime
from src.trends_fetcher import get_trending_script_topic


def generate_script(match_text=None, all_stories=None):
    topic = get_trending_script_topic("kids")

    title = f"{topic.title()} - Amazing Facts For Kids!"

    paragraphs = [
        f"Welcome to our kids channel! Today is {datetime.now().strftime('%B %d, %Y')}, and we have something really special for you. Get ready to learn about {topic}!",
        f"Have you ever wondered about {topic}? Well, today we're going to explore this amazing topic together. Kids all around the world love learning about new things, and you're about to discover something incredible!",
        f"Scientists study {topic} every day to learn more about our amazing world. From the deepest oceans to the farthest stars, there's so much to discover. And guess what? You can be a scientist too, just by asking questions and being curious!",
        f"Did you know that learning about {topic} can be super fun? There are so many cool facts and interesting stories waiting for you. Share what you learn today with your friends and family - they'll be amazed!",
        f"Parents love it when kids learn new things. So by watching this video, you're not just having fun - you're also becoming smarter! Keep exploring, keep asking questions, and never stop being curious about the world around you.",
        f"Thanks for watching! If you enjoyed learning about {topic}, make sure to subscribe for more amazing videos. There's always something new to discover, so come back soon for more fun learning adventures!",
    ]

    return {
        "title": title,
        "script": "\n\n".join(paragraphs),
        "description": f"Join us on an amazing journey to learn about {topic}! This fun and educational video is perfect for kids who love to discover new things. Watch, learn, and share with your friends!\n\n#kids #learning #funfacts #education #kidschannel",
        "tags": ["kids", "learning", "fun facts", "education", "children", topic],
        "category": "24",
    }
