import random
from datetime import datetime

TEMPLATES = [
    {
        "title": "Amazing Animal Facts for Smart Kids! #kids #animals #funfacts",
        "script": f"Hello kids! Welcome to Fun Facts Daily. Today is {datetime.now().strftime('%B %d, %Y')}, and we have the most amazing animal facts that will blow your mind!\n\nDid you know that octopuses have THREE hearts? Two pump blood to the gills, and one pumps it to the body. When they swim, the heart that pumps blood to the body stops beating! That's why they prefer to crawl.\n\nAnd here's another cool fact: butterflies taste with their feet! They have taste sensors on their legs, so when they land on a flower, they can taste it immediately.\n\nAlso, did you know that honey never spoils? Archaeologists found 3,000-year-old honey in ancient Egyptian tombs and it was still edible!\n\nBananas are technically berries, but strawberries are NOT! A berry has seeds inside, not outside.\n\nThe biggest star in the universe is called UY Scuti. It's so huge it would swallow everything up to Saturn if it were our sun!\n\nSubscribe now for more amazing fun facts every day! Learn something new and impress your friends!",
        "tags": ["kids", "animals", "funfacts", "education", "learning", "science", "nature", "children"],
        "description": "Amazing fun facts for kids! Learn about octopus hearts, butterfly feet, honey, and more! Subscribe for daily fun facts!",
    },
    {
        "title": "Space Facts That Will Blow Your Mind! #kids #space #science",
        "script": f"Hello space explorers! Today is {datetime.now().strftime('%B %d, %Y')} and we are going on an amazing journey through space!\n\nDid you know that the Sun is 400 times bigger than the Moon? But it also is 400 times farther away, so they look the same size in the sky! Perfect cosmic coincidence!\n\nA day on Venus is longer than a year on Venus! Venus takes 243 Earth days to rotate once, but only 225 Earth days to orbit the Sun.\n\nThere are more stars in the universe than grains of sand on all the beaches on Earth!\n\nFootprints on the Moon will stay there for millions of years because there is no wind or water to wash them away.\n\nSpace is completely silent because there is no air to carry sound waves.\n\nSubscribe now for more amazing space facts! The universe is full of wonders!",
        "tags": ["kids", "space", "science", "education", "funfacts", "learning", "astronomy", "children"],
        "description": "Amazing space facts for kids! Learn about the Sun, Moon, stars, and more! Subscribe for daily space facts!",
    },
    {
        "title": "Crazy Science Experiments You Can Try! #kids #science #diy",
        "script": f"Hello young scientists! Today is {datetime.now().strftime('%B %d, %Y')} and we have amazing science facts and experiments for you!\n\nDid you know you can make a volcano at home? Mix baking soda and vinegar and watch it erupt!\n\nDid you know that water can freeze and boil at the same time? It's called the triple point!\n\nHot water freezes faster than cold water! This is called the Mpemba effect.\n\nA cloud can weigh more than a million pounds! Even though it looks fluffy and light.\n\nTrees can talk to each other through underground networks called the Wood Wide Web!\n\nYour brain uses 20% of your body's energy even though it's only 2% of your weight!\n\nSubscribe for more amazing science facts and experiments!",
        "tags": ["kids", "science", "experiments", "education", "learning", "funfacts", "diy", "children"],
        "description": "Amazing science facts for kids! Learn about volcanoes, water, clouds, and more! Subscribe for daily science!",
    },
    {
        "title": "Ocean Wonders: Sea Creatures Facts! #kids #ocean #animals",
        "script": f"Hello ocean explorers! Today is {datetime.now().strftime('%B %d, %Y')} and we are diving deep into the ocean to meet amazing sea creatures!\n\nDid you know that the blue whale is the largest animal that has ever lived on Earth? It's bigger than the biggest dinosaur!\n\nOctopuses have three hearts and blue blood! Their blood is blue because it contains copper instead of iron.\n\nStarfish can regrow their arms! If a starfish loses an arm, it can grow a new one.\n\nSea horses are the only animals where the MALE gives birth! The father carries the babies in a pouch.\n\nJellyfish have been around for over 500 million years - that's before dinosaurs!\n\nThe ocean covers 71% of Earth's surface but we've explored less than 20% of it.\n\nSubscribe for more amazing ocean facts!",
        "tags": ["kids", "ocean", "animals", "education", "learning", "funfacts", "nature", "children"],
        "description": "Amazing ocean facts for kids! Learn about whales, octopuses, starfish, and more! Subscribe for daily ocean facts!",
    },
]


def generate_script(match_text="", stories=None):
    template = random.choice(TEMPLATES)
    return {
        "title": template["title"],
        "script": template["script"],
        "tags": template["tags"],
        "description": template["description"],
    }


if __name__ == "__main__":
    data = generate_script()
    print(f"Title: {data['title']}")
    print(f"Description: {data['description']}")