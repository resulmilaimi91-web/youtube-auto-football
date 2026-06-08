import random
from datetime import datetime

TEMPLATES = [
    {
        "title": "Këto janë Lajmet e Fundit nga Bota e Futbollit! ⚽",
        "description": "Golat më të bukur, transferimet më të nxehta dhe analizat ekskluzive. Mos i humb!",
        "tags": ["futboll", "football", "highlights", "gola", "shqiperi", "laliga", "premierleague", "championsleague"],
    },
    {
        "title": "Top 5 Golat e Javës që S'Po i Harroni Dot! 🔥",
        "description": "Golat më spektakolar të kësaj jave në Premier League, La Liga, Serie A dhe më shumë!",
        "tags": ["gola", "highlights", "futboll", "topgola", "premierleague", "footballshorts"],
    },
    {
        "title": "Çfarë Ndodhi Sot në Botën e Futbollit? ⚡",
        "description": "Përmbledhja e lajmeve më të fundit nga futbolli botëror. Abonohu për më shumë!",
        "tags": ["futboll", "footballnews", "highlights", "sport", "shqiperi"],
    },
]

def generate_script(match_text, stories):
    template = random.choice(TEMPLATES)
    date_str = datetime.now().strftime("%d %B %Y")

    body_parts = [f"Përshëndetje miq të dashur! Sot është {date_str} dhe kemi lajme të nxehta."]

    if match_text and "nuk ka ndeshje" not in match_text:
        body_parts.append("\nNdeshjet e sotme:")
        body_parts.append(match_text)

    if stories:
        body_parts.append("\nLajmet kryesore:")
        for i, s in enumerate(stories[:3], 1):
            body_parts.append(f"{i}. {s}")

    body_parts.append("\nÇfarë mendoni për këto lajme? Shkruani në komente!")
    body_parts.append("Mos harroni të abonoheni për të mos humbur asnjë video!")

    script = "\n\n".join(body_parts)
    return {
        "title": template["title"],
        "description": template["description"] + f"\n\n📅 {date_str}\n\n#futboll #football #highlights",
        "tags": template["tags"],
        "script": script,
    }
