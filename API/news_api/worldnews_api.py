import requests
import urllib.parse

def search_world_news(keywords, starting_date, ending_date, language="en"):
    """
    Search articles using World News API with multiple keywords (ORed together).
    
    Parameters
    ----------
    keywords : list of str
        Keywords to search for. The search will match any of these (using OR).
    starting_date : str
        Earliest publish date, format YYYY-MM-DD.
    ending_date : str
        Latest publish date, format YYYY-MM-DD.
    language : str, optional
        Language code, default "en".
    """
    api_key = "96c129136e4d47ae9f6234455a0841fd"
    base_url = "https://api.worldnewsapi.com/search-news"
    
    # Build the text parameter: join keywords with ' OR '
    text_query = " OR ".join(keywords)
    # URL-encode it
    text_param = urllib.parse.quote(text_query)
    
    params = {
        "text": text_param,
        "language": language,
        "earliest-publish-date": starting_date,
        "latest-publish-date": ending_date  # if this param is supported
    }
    headers = {
        "x-api-key": api_key
    }
    
    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

if __name__ == "__main__":
    result = search_world_news(
        keywords=["earthquake", "tsunami", "volcanic eruption"],
        starting_date="2025-11-01",
        ending_date="2025-11-03"
    )
    print(result)
