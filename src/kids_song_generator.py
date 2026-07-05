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
        "educational": False,
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
        "educational": False,
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
        "educational": True,
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
        "educational": False,
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
        "educational": True,
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
        "educational": False,
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
        "educational": False,
    },
    {
        "title": "ABC Animal Song",
        "lyrics": [
            "A is for Alligator, snap snap snap",
            "B is for Bear taking a nap",
            "C is for Cat with fur so soft",
            "D is for Dog running far aloft",
            "",
            "E is for Elephant so big and strong",
            "F is for Fox singing along",
            "G is for Giraffe with neck so tall",
            "H is for Horse having a ball",
            "",
            "I is for Iguana sitting in the sun",
            "J is for Jaguar on the run",
            "K is for Kangaroo jumping high",
            "L is for Lion with a mighty cry",
            "",
            "M is for Monkey swinging in a tree",
            "N is for Newt as small as can be",
            "O is for Owl hooting at night",
            "P is for Penguin dressed in white",
            "",
            "Q is for Queen Bee buzzing around",
            "R is for Rabbit hopping on the ground",
            "S is for Snake slithering slow",
            "T is for Turtle taking it slow",
            "",
            "U is for Umbrella Bird with a fancy crest",
            "V is for Vulture flying with the rest",
            "W is for Whale swimming in the sea",
            "X is for X-ray Fish for you and me",
            "",
            "Y is for Yak with wool so thick",
            "Z is for Zebra with a stripe trick",
            "Now we know our ABCs",
            "Sing with animals if you please",
        ],
        "color": (100, 255, 150),
        "theme": "abc",
        "educational": True,
    },
    {
        "title": "Ten Little Numbers",
        "lyrics": [
            "One little two little three little numbers",
            "Four little five little six little numbers",
            "Seven little eight little nine little numbers",
            "Ten little numbers we know",
            "",
            "One is for a single sun in the sky",
            "Two is for a pair of butterflies",
            "Three is for three little kittens at play",
            "Four is for four ducks swimming away",
            "",
            "Five is for five fingers on one hand",
            "Six is for six castles in the sand",
            "Seven is for seven stars so bright",
            "Eight is for eight kites taking flight",
            "",
            "Nine is for nine flowers in a row",
            "Ten is for ten little toes you know",
            "Count with me from one to ten",
            "Let's all count them once again",
            "",
            "One little two little three little numbers",
            "Four little five little six little numbers",
            "Seven little eight little nine little numbers",
            "Ten little numbers we know",
        ],
        "color": (255, 200, 50),
        "theme": "numbers",
        "educational": True,
    },
    {
        "title": "Shapes All Around",
        "lyrics": [
            "A circle is round like the sun in the sky",
            "A square has four sides, my oh my",
            "A triangle has three sides you see",
            "A rectangle is great for you and me",
            "",
            "Circle circle round and round",
            "Square square on the ground",
            "Triangle triangle pointy and neat",
            "Rectangle rectangle what a treat",
            "",
            "A diamond sparkles like a star so bright",
            "An oval shape is quite a sight",
            "A heart shape means I love you so",
            "A star shape makes our spirits glow",
            "",
            "Shapes are everywhere we go",
            "In the sky and down below",
            "Learn your shapes and you will see",
            "How fun the world can be",
        ],
        "color": (255, 150, 200),
        "theme": "shapes",
        "educational": True,
    },
    {
        "title": "Days of the Week Song",
        "lyrics": [
            "Monday Monday starts the week",
            "Time to learn and time to speak",
            "Tuesday Tuesday comes along",
            "Sing with us a happy song",
            "",
            "Wednesday Wednesday in the middle",
            "Play a tune upon the fiddle",
            "Thursday Thursday almost there",
            "Friday Friday beyond compare",
            "",
            "Saturday Saturday time for fun",
            "Playing games under the sun",
            "Sunday Sunday rest and play",
            "Enjoy your family every day",
            "",
            "Seven days make one full week",
            "Every day is what we seek",
            "Monday Tuesday Wednesday too",
            "Thursday Friday for me and you",
            "",
            "Saturday Sunday fun and rest",
            "Every day we try our best",
            "Now you know the days so fine",
            "Seven days in a straight line",
        ],
        "color": (150, 200, 255),
        "theme": "days",
        "educational": True,
    },
    {
        "title": "Head Shoulders Knees and Toes",
        "lyrics": [
            "Head and shoulders knees and toes",
            "Knees and toes",
            "Head and shoulders knees and toes",
            "Knees and toes",
            "",
            "Eyes and ears and mouth and nose",
            "Head and shoulders knees and toes",
            "Knees and toes",
            "",
            "Arms and hands and fingers ten",
            "Let me count them once again",
            "Legs and feet and ten small toes",
            "Wiggle wiggle your little nose",
            "",
            "Elbows bending left and right",
            "Wrists and ankles out of sight",
            "Hips and back and neck so strong",
            "Sing your body song along",
            "",
            "Head and shoulders knees and toes",
            "Knees and toes",
            "Head and shoulders knees and toes",
            "Knees and toes",
        ],
        "color": (100, 255, 200),
        "theme": "body",
        "educational": True,
    },
    {
        "title": "Fruit Song Yummy Yummy",
        "lyrics": [
            "Apples are red and apples are sweet",
            "A yummy fruit that's fun to eat",
            "Bananas are yellow, so soft and long",
            "Eating a banana makes us strong",
            "",
            "Oranges are orange, juicy and round",
            "The sweetest fruit that can be found",
            "Grapes are purple or green you know",
            "In a bunch they love to grow",
            "",
            "Strawberries are red with tiny seeds",
            "A yummy fruit for all our needs",
            "Watermelon green on the outside",
            "Red and sweet is what's inside",
            "",
            "Fruits are healthy, fruits are great",
            "Eat them all, don't make us wait",
            "Every color every taste",
            "A yummy fruit is never waste",
        ],
        "color": (255, 100, 150),
        "theme": "fruits",
        "educational": True,
    },
    {
        "title": "Weather Song",
        "lyrics": [
            "Sunny sunny day so bright",
            "Let's go outside, what a sight",
            "Cloudy cloudy in the sky",
            "Fluffy clouds go drifting by",
            "",
            "Rainy rainy drop drop drop",
            "Pitter patter never stop",
            "Windy windy blow blow blow",
            "Watch the leaves go to and fro",
            "",
            "Snowy snowy white and cold",
            "Winter stories to be told",
            "Stormy stormy thunder crash",
            "Lightning with a brilliant flash",
            "",
            "Weather changes every day",
            "Come outside and let's all play",
            "Sun or rain or snow or breeze",
            "Every weather makes us please",
        ],
        "color": (150, 150, 255),
        "theme": "weather",
        "educational": True,
    },
    {
        "title": "Vroom Vroom Vehicles",
        "lyrics": [
            "Vroom vroom the car goes fast",
            "Driving by will never last",
            "Beep beep the bus is here",
            "Picking up kiddies far and near",
            "",
            "Choo choo the train on the track",
            "Clickety clack clickety clack",
            "Zoom zoom the airplane flies",
            "Soaring up into the skies",
            "",
            "Ring ring the bicycle bell",
            "Riding through the town as well",
            "Splash splash the boat goes by",
            "Sailing under a sunny sky",
            "",
            "Fire truck goes wee woo wee",
            "Helping everyone you see",
            "Digger digger scoop the ground",
            "Making piles all around",
            "",
            "Vehicles go fast and slow",
            "Watch them travel to and fro",
            "On the road or in the air",
            "Vehicles are everywhere",
        ],
        "color": (255, 180, 50),
        "theme": "vehicles",
        "educational": True,
    },
]

DESCRIPTION_TEMPLATES = [
    "Sing along with {title}! This fun and educational kids song is perfect for toddlers, preschoolers, and young children. Learn while you play with our original music and colorful animations!",
    "{title} - a brand new original kids song that makes learning fun! Dance, sing, and discover with our friendly characters. Perfect for early childhood education and family entertainment.",
    "It's time to sing and learn with {title}! Our original kids songs help children develop language skills, creativity, and a love for music. Made with love for kids everywhere!",
    "Join us for {title}! This educational video encourages singing, dancing, and learning. All content is original, safe, and created to inspire young minds.",
]

HASHTAGS_ALL = [
    "#kidssong", "#nurseryrhyme", "#singalong", "#kidsmusic", "#toddler",
    "#preschool", "#childrensongs", "#kidsvideo", "#learning", "#funforkids",
    "#educational", "#babysongs", "#originalmusic", "#cortana", "#kidsentertainment",
]

KEYWORDS_ALL = [
    "kidssong", "nurseryrhyme", "singalong", "kidsmusic",
    "toddler", "preschool", "childrensongs", "kidsvideo",
    "learning", "funforkids", "educational", "babysongs",
    "animation", "cortana songs", "original kids song",
]


def generate_song():
    preferred = _get_preferred_theme()

    if preferred == "educational":
        educational = [t for t in SONG_TEMPLATES if t["educational"]]
        template = random.choice(educational) if educational else random.choice(SONG_TEMPLATES)
    elif preferred:
        matching = [t for t in SONG_TEMPLATES if t["theme"] == preferred]
        if matching:
            template = matching[0]
        else:
            template = random.choice(SONG_TEMPLATES)
    else:
        template = random.choice(SONG_TEMPLATES)

    title = template["title"]
    full_lyrics = "\n".join(template["lyrics"])

    desc_template = random.choice(DESCRIPTION_TEMPLATES)
    desc_base = desc_template.format(title=title)

    tags_extra = []
    if template["educational"]:
        tags_extra = ["learncolors", "learnnumbers", "learnshapes", "abcsong",
                      "counting", "educationalvideo"]
    else:
        tags_extra = ["animalsforkids", "funforkids", "singalongforkids"]

    hashtags = random.sample(HASHTAGS_ALL, min(8, len(HASHTAGS_ALL)))
    description = (
        f"{desc_base}\n\n"
        f"🔔 Don't forget to SUBSCRIBE for more fun songs every day!\n"
        f"👍 Like and Share if you enjoyed this video!\n\n"
        f"📚 More Kids Songs:\n"
        f"🎵 The Rainbow Song\n"
        f"🎵 Counting Stars\n"
        f"🎵 Bunny Hop Hop\n"
        f"🎵 ABC Animal Song\n"
        f"🎵 Ten Little Numbers\n\n"
        f"{' '.join(hashtags)}"
    )

    tags = KEYWORDS_ALL + tags_extra

    return {
        "title": title,
        "script": full_lyrics,
        "lyrics": template["lyrics"],
        "description": description,
        "tags": tags,
        "category": "24",
        "theme": template["theme"],
        "bg_color": template["color"],
        "educational": template["educational"],
    }
