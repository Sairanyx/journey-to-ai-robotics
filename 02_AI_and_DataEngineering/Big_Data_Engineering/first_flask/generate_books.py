import random
import requests

URL = "http://127.0.0.1:5000/sell/"

first_names = ["Esteri", "Matti", "Aino", "Leo", "Sofia"]
last_names = ["Korhonen", "Virtanen", "Nieminen", "Laine", "Heikkinen"]
title_words = ["Robot", "Data", "Ocean", "Future", "Dream"]

for i in range(100):
    book = {
        "title": f"{random.choice(title_words)} {random.choice(title_words)}",
        "author": f"{random.choice(first_names)} {random.choice(last_names)}",
        "year_of_publication": random.randint(1950, 2026)
    }

    r = requests.post(URL, json=book)

    print(i + 1, r.status_code, r.json())




