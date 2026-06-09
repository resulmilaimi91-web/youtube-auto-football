import os
import random
from datetime import datetime


def generate_ai_script(match_text="", stories=None, topic_hint=""):
    script = None

    script = _try_huggingface(match_text, stories, topic_hint)
    if script:
        return _build_result(script, topic_hint)

    script = _try_groq(match_text, stories, topic_hint)
    if script:
        return _build_result(script, topic_hint)

    return None


def _try_huggingface(match_text="", stories=None, topic_hint=""):
    try:
        import urllib.request
        import json

        api_key = os.environ.get("HF_TOKEN", "")
        date_str = datetime.now().strftime("%B %d, %Y")

        context = f"Today is {date_str}."
        if match_text:
            context += f"\nLatest matches: {match_text}"
        if stories:
            context += f"\nRecent news: {'; '.join(stories[:3])}"

        prompt = f"""You are a professional football news anchor for YouTube.

{context}

Write a 250-word script about FIFA World Cup 2026. Be professional, engaging, natural like a TV news anchor. No emojis. No markdown. Just spoken English.

Script:"""

        payload = json.dumps({
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 512,
                "temperature": 0.7,
                "do_sample": True,
                "return_full_text": False,
            }
        }).encode()

        headers = {
            "Authorization": f"Bearer {api_key}" if api_key else "",
            "Content-Type": "application/json",
        }

        models = [
            "mistralai/Mistral-7B-Instruct-v0.3",
            "HuggingFaceH4/zephyr-7b-beta",
            "google/gemma-2-2b-it",
        ]

        for model in models:
            try:
                url = f"https://api-inference.huggingface.co/models/{model}"
                req = urllib.request.Request(url, data=payload, headers={k: v for k, v in headers.items() if v}, method="POST")
                resp = urllib.request.urlopen(req, timeout=60)
                result = json.loads(resp.read())

                if isinstance(result, list) and len(result) > 0:
                    generated = result[0].get("generated_text", "")
                    if len(generated) > 100:
                        return generated.strip()
            except Exception:
                continue

        return None

    except Exception as e:
        print(f"HuggingFace failed: {e}")
        return None


def _try_groq(match_text="", stories=None, topic_hint=""):
    try:
        import urllib.request
        import json

        api_key = os.environ.get("GROQ_API_KEY", "")
        if not api_key:
            return None

        date_str = datetime.now().strftime("%B %d, %Y")

        context = f"Today is {date_str}."
        if match_text:
            context += f"\nLatest matches: {match_text}"
        if stories:
            context += f"\nRecent news: {'; '.join(stories[:3])}"

        prompt = f"""You are a professional football news anchor for YouTube.

{context}

Write a 250-word script about FIFA World Cup 2026. Be professional, engaging, natural like a TV news anchor. No emojis. No markdown. Just spoken English.

Script:"""

        payload = json.dumps({
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512,
            "temperature": 0.7,
        }).encode()

        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=payload,
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        )
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())

        content = result["choices"][0]["message"]["content"]
        if len(content) > 100:
            return content.strip()

        return None

    except Exception as e:
        print(f"Groq failed: {e}")
        return None


def _build_result(script, topic_hint=""):
    if len(script) < 100:
        return None

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
    title = random.choice(titles)

    first_200 = script[:200].replace("\n", " ")
    description = f"""{first_200}...

SUBSCRIBE for daily World Cup 2026 coverage!
LIKE to support the channel!
COMMENT your predictions!

#worldcup2026 #fifa #football #soccer #worldcup #footballnews #highlights #sports #football2026 #fifaworldcup"""

    tags = ["worldcup2026", "fifa", "worldcup", "football", "soccer", "footballnews", "sports"]
    extras = random.sample(["highlights", "footballhighlights", "worldcup2026", "fifaworldcup", "2026worldcup", "dailyfootball", "dailysoccer"], 5)
    tags.extend(extras)

    hashtags = ["worldcup2026", "fifa", "football", "soccer", "worldcup"]

    return {
        "title": title,
        "description": description,
        "tags": tags,
        "hashtags": hashtags,
        "script": script,
    }


if __name__ == "__main__":
    result = generate_ai_script()
    if result:
        print("Title:", result["title"])
        print("Script:", result["script"][:200] + "...")
    else:
        print("No AI available, using templates")
