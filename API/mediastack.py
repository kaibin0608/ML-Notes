# Python 3
import http.client, urllib.parse
import json

conn = http.client.HTTPConnection('api.mediastack.com')

params = urllib.parse.urlencode({
    'access_key': '194e6621af46ede627504fd9e95d2f36',
    # 'keywords': 'KL',
    'languages': 'zh',
    'countries': 'my',
    'categories': '-general,-sports',
    'sort': 'published_desc',
    'limit': 1,
    })

conn.request('GET', '/v1/news?{}'.format(params))

res = conn.getresponse()
data = res.read().decode('utf-8')

# Parse JSON
response_json = json.loads(data)
print("Full response:", response_json)

# Check that 'data' exists
if 'data' in response_json:
    for article in response_json['data']:
        print("\nTitle: " + article.get('title'))
        print("Author: " + article.get('author'))
        print("URL: " + article.get('url'))
        print("Language: " + article.get('language'))
        print("Country: " + article.get('country'))