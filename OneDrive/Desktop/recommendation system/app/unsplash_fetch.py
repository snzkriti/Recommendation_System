import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")


def get_unsplash_data(keyword):

    url = "https://api.unsplash.com/search/photos"

    params = {
        "query": keyword,
        "per_page": 1,
        "client_id": ACCESS_KEY
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    if not data["results"]:
        return None

    item = data["results"][0]

    return {
        "keyword": keyword,
        "image_url": item["urls"]["regular"],
        "description": item.get(
            "alt_description",
            keyword
        )
    }