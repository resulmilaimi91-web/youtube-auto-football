import os
import random
import json
from datetime import datetime


def generate_ai_script(match_text="", stories=None, topic_hint=""):
    try:
        import anthropic
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return None

        client = anthropic.Anthropic(api_key=api_key)

        date_str = datetime.now().strftime("%B %d, %Y")

        context = f"Today is {date_str}."
        if match_text:
            context += f"\nLatest matches: {match_text}"
        if stories:
            context += f"\nRecent news: {'; '.join(stories[:3])}"
        if topic_hint:
            context += f"\nFocus topic: {topic_hint}"

        prompt = f"""You are a professional football news anchor for a YouTube channel called "Football Highlights Daily".

{context}

Create a video script about the FIFA World Cup 2026. Requirements:
- Start with a professional greeting mentioning today's date
- Speak in a natural, engaging news anchor tone
- Include 3-5 key football news stories or World Cup 2026 updates
- Use transitional phrases between segments
- End with a call to action (subscribe, comment, like)
- Write as if speaking to camera, conversational but professional
- Keep it between 200-350 words
- Do NOT use any emojis
- Do NOT use markdown formatting
- Use periods and commas for natural pauses
- Write in English

Script:"""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        script = message.content[0].text.strip()

        if len(script) < 100:
            return None

        title = _extract_title(script, topic_hint)
        description = _create_description(title, script)
        tags = _create_tags(title)
        hashtags = _create_hashtags(title)

        return {
            "title": title,
            "description": description,
            "tags": tags,
            "hashtags": hashtags,
            "script": script,
        }

    except Exception as e:
        print(f"Claude API failed: {e}")
        return None


def _extract_title(script, hint=""):
    titles = [
        "FIFA WORLD CUP 2026: Complete Guide To The Biggest Event!",
        "World Cup 2026 Host Cities: Full Stadium Tour!",
        "World Cup 2026: Every Team That Has Qualified!",
        "World Cup 2026: New 48-Team Format Explained!",
        "Top 10 Players Who Will Dominate World Cup 2026!",
        "World Cup 2026: Who Will Win The Trophy?",
        "Today's Football News + World Cup 2026 Updates!",
        "World Cup 2026: Match Schedule And Key Dates!",
        "World Cup 2026: Prize Money And Rewards Revealed!",
        "World Cup 2026: Latest Qualification Results!",
    ]
    return random.choice(titles)


def _create_description(title, script):
    first_100 = script[:200].replace("\n", " ")
    return f"""{first_100}...

SUBSCRIBE for daily World Cup 2026 coverage!
LIKE to support the channel!
COMMENT your predictions!

#worldcup2026 #fifa #football #soccer #worldcup #footballnews #highlights #sports #football2026 #fifaworldcup"""


def _create_tags(title):
    base = ["worldcup2026", "fifa", "worldcup", "football", "soccer", "footballnews", "sports"]
    extras = random.sample(["highlights", "footballhighlights", "worldcup2026", "fifaworldcup", "2026worldcup", "dailyfootball", "dailysoccer"], 5)
    return base + extras


def _create_hashtags(title):
    base = ["worldcup2026", "fifa", "football", "soccer", "worldcup"]
    return base


if __name__ == "__main__":
    result = generate_ai_script()
    if result:
        print("Title:", result["title"])
        print("Script:", result["script"][:200] + "...")
