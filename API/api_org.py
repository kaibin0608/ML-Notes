from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key='3c6473a7cb6d404f8122e7c3beb29ec1')

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(
                                        #   sources='bbc-news,the-verge',
                                          category='business',
                                          language='zh',
                                          country='my',
                                          page = 1)

# /v2/everything
all_articles = newsapi.get_everything(q='Kuala Lumpur',
                                    #   sources='my',
                                    #   sources='bbc-news,the-verge',
                                    #   domains='bbc.co.uk,techcrunch.com',
                                      from_param='2025-10-01',
                                      to='2025-10-27',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

# /v2/top-headlines/sources
sources = newsapi.get_sources()

print(top_headlines)
# print(sources)