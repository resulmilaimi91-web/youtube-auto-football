import random
import json
import os

STRATEGY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content_strategy.json")


def _get_preferred_theme():
    try:
        if os.path.exists(STRATEGY_FILE):
            with open(STRATEGY_FILE) as f:
                strategy = json.load(f)
            themes = strategy.get("recommended_themes", [])
            if themes:
                return themes[0]
    except Exception:
        pass
    return None


SONG_TEMPLATES = [
    {
        "title": "The Rainbow Song",
        "lyrics": [
            "Red and orange, yellow too",
            "Green and blue and purple hue",
            "Rainbow shining in the sky",
            "Watch it dance, way up high",
            "",
            "After rain the sun appears",
            "Wiping away all our tears",
            "Colors bright for you and me",
            "Rainbow, rainbow, wild and free",
            "",
            "Red like apples on a tree",
            "Orange like the sun you see",
            "Yellow like a happy star",
            "Green like grass not very far",
            "",
            "Blue like ocean deep and wide",
            "Purple like a butterfly's ride",
            "Rainbow, rainbow, in the sky",
            "Wave goodbye as you fly by",
        ],
        "color": (255, 100, 100),
        "theme": "rainbow",
    },
    {
        "title": "Bunny Hop Hop",
        "lyrics": [
            "Little bunny soft and sweet",
            "Hoppity hop on tiny feet",
            "Ears so long and tail so small",
            "You are the cutest of them all",
            "",
            "Bunny hops across the grass",
            "Letting all the moments pass",
            "Nibbles on a carrot treat",
            "Such a lovely friend to meet",
            "",
            "Hop hop hop from left to right",
            "Bunny dances in the light",
            "Fluffy white or brown or gray",
            "Happy bunny every day",
            "",
            "When the sun goes down to rest",
            "Bunny curls up in its nest",
            "Close your eyes and dream so deep",
            "Sweet dreams bunny, time to sleep",
        ],
        "color": (255, 200, 150),
        "theme": "bunny",
    },
    {
        "title": "Counting Stars",
        "lyrics": [
            "One little star up in the sky",
            "Two little stars go twinkling by",
            "Three little stars so warm and bright",
            "Four little stars light up the night",
            "",
            "Five little stars they dance with glee",
            "Six little stars for you and me",
            "Seven stars, oh what a sight",
            "Eight little stars so big and bright",
            "",
            "Nine stars shining from afar",
            "Ten little stars, there you are",
            "Count the stars up in the sky",
            "Let's all sing and let's all try",
            "",
            "Stars above so very high",
            "Twinkle twinkle, blink and sigh",
            "Now we've counted one to ten",
            "Let's all count them once again",
        ],
        "color": (100, 100, 255),
        "theme": "stars",
    },
    {
        "title": "Happy Little Fish",
        "lyrics": [
            "Swimmy swimmy little fish",
            "Dancing in the water dish",
            "Fins so shiny, tail so fast",
            "Happy moments that will last",
            "",
            "Bubbles floating to the top",
            "Never gonna let you drop",
            "Orange, yellow, blue and red",
            "Little fish go straight ahead",
            "",
            "Underwater world so grand",
            "Castles made of golden sand",
            "Plants that wave and rocks so tall",
            "Little fish loves one and all",
            "",
            "Splash around and have some fun",
            "Playing in the morning sun",
            "Little fish I love you so",
            "Watch you swim and watch you grow",
        ],
        "color": (100, 200, 255),
        "theme": "fish",
    },
    {
        "title": "The Color Train",
        "lyrics": [
            "Choo choo train is on its way",
            "Bringing colors every day",
            "First car red, so big and bright",
            "Second car is orange light",
            "",
            "Third car yellow like the sun",
            "Fourth car green, the ride's so fun",
            "Fifth car blue up in the sky",
            "Sixth car purple waving by",
            "",
            "Choo choo train goes down the track",
            "Come along, there's no turning back",
            "Colors fill the world around",
            "Happiness can be found",
            "",
            "Now the train has reached the end",
            "But colors will forever blend",
            "Choo choo, goodbye my friend",
            "Our color ride will never end",
        ],
        "color": (255, 150, 50),
        "theme": "train",
    },
    {
        "title": "Kitty Cat Song",
        "lyrics": [
            "Soft little kitty with fur so warm",
            "Cuddled up in perfect form",
            "Whiskers twitch and eyes so green",
            "Cutest kitty ever seen",
            "",
            "Pitter patter little feet",
            "Playing in the window seat",
            "Chasing yarn and balls of string",
            "Happiness that you bring",
            "",
            "Purring like a tiny drum",
            "Underneath my thumb you come",
            "Nap time in the warm sun ray",
            "Sleepy kitty all the day",
            "",
            "When the moon begins to glow",
            "Kitty's ready for the show",
            "Dancing in the silver light",
            "Goodnight kitty, sleep so tight",
        ],
        "color": (200, 150, 255),
        "theme": "cat",
    },
    {
        "title": "Morning Sunshine",
        "lyrics": [
            "Wake up wake up sleepy head",
            "Time to get out of your bed",
            "Sun is shining through the glass",
            "New day starting, let it pass",
            "",
            "Brush your teeth and comb your hair",
            "Put on clothes with greatest care",
            "Breakfast time with milk and bread",
            "Happy thoughts inside your head",
            "",
            "Go outside and feel the breeze",
            "Playing underneath the trees",
            "Birds are singing in the sky",
            "Butterflies are flying by",
            "",
            "Evening comes and day is done",
            "What a lovely day of fun",
            "Time to rest and close your eyes",
            "Morning comes with new surprise",
        ],
        "color": (255, 220, 100),
        "theme": "morning",
    },
]


def generate_song():
    preferred = _get_preferred_theme()
    if preferred:
        matching = [t for t in SONG_TEMPLATES if t["theme"] == preferred]
        if matching:
            template = matching[0]
        else:
            template = random.choice(SONG_TEMPLATES)
    else:
        template = random.choice(SONG_TEMPLATES)

    title = template["title"]

    full_lyrics = "\n".join(template["lyrics"])

    description = (
        f"Sing along with our fun original kids song - {title}! "
        f"This educational video is perfect for toddlers, "
        f"preschoolers, and young children. All content is original and created "
        f"for learning and entertainment. Dance, sing, and learn with us!\n\n"
        f"#kidssong #nurseryrhyme #singalong #kidsmusic #toddler #preschool #childrensongs"
    )

    tags = [
        "kidssong", "nurseryrhyme", "singalong", "kidsmusic",
        "toddler", "preschool", "childrensongs", "kidsvideo",
        "learning", "funforkids",
    ]

    return {
        "title": title,
        "script": full_lyrics,
        "lyrics": template["lyrics"],
        "description": description,
        "tags": tags,
        "category": "24",
        "theme": template["theme"],
        "bg_color": template["color"],
    }
