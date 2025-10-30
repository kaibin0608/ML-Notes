import requests
import json
from datetime import datetime 

API_KEY = "f294630ecbde0941487bcf33b70b8d9f"
BASE_URL = "https://gnews.io/api/v4"

def search_news(query, lang="en", country=None, max_results=5):
    params = {
        "q": query,
        # "lang": lang,
        "max": max_results,
        "apikey": API_KEY
    }
    if country:
        params["country"] = country

    url = f"{BASE_URL}/search"
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data.get("articles", [])

def print_articles(articles):
    for art in articles:
        print("Title:", art.get("title"))
        print("Source:", art.get("source", {}).get("name"))
        print("Published At:", art.get("publishedAt"))
        print("URL:", art.get("url"))
        print("----")

if __name__ == "__main__":
    query = "Suruhanjaya Syarikat Malaysia"
    print(f"Searching GNews for: {query}")
    articles = search_news(query, lang="en", country="my", max_results=10)
    print(f"Found {len(articles)} articles.")
    print_articles(articles)