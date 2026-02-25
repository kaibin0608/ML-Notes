# Make a GET request to 'python.org', using Requests:
from requests_html import HTMLSession
session = HTMLSession()
r = session.get('https://python.org/')

# extract links
links = r.html.links
absolute_links = r.html.absolute_links

# Extract with CSS
about = r.html.find('#about', first=True)
print(about.find('a'))

# Try async and get some sites at the same time:
from requests_html import AsyncHTMLSession
asession = AsyncHTMLSession()
async def get_pythonorg():
    r = await asession.get('https://python.org/')
    return r

async def get_reddit():
    r = await asession.get('https://reddit.com/')
    return r

async def get_google():
    r = await asession.get('https://google.com/')
    return r
results = asession.run(get_pythonorg, get_reddit, get_google)
print(results)

# Note that the order of the objects in the results list represents the order they were returned in, 
# not the order that the coroutines are passed to the run method, which is shown in the example by the order being different.
for result in results:
    print(result.html.url)

