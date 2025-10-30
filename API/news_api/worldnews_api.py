import worldnewsapi 
# from worldnewsapi.rest import ApiException

"""Run the news API scraper to fetch SSM-related news."""
# api_key = "0d033f49793b4de5a06b3cf353d2ed80"
base_url = "https://api.worldnewsapi.com/search-news-sources"

# Initial SDK configuration
newsapi_configuration = worldnewsapi.Configuration(api_key={'apiKey': "0d033f49793b4de5a06b3cf353d2ed80"})

try:
	newsapi_instance = worldnewsapi.NewsApi(worldnewsapi.ApiClient(newsapi_configuration))

	max_results = 250   # replace with your maximum
	offset = 0
	all_results = []

	while len(all_results) < max_results:

		request_count = min(100, max_results - len(all_results)) # request 100 or the remaining number of articles

		response = newsapi_instance.search_news(
			# name = "orientaldaily"
			text='SSM',
			source_country='my',
			# language='zh',
			earliest_publish_date='2025-10-01',
			latest_publish_date='2025-10-30',
			# # categories='sports',
			sort="publish-time",
			sort_direction="desc",
			min_sentiment=-0.8,
			max_sentiment=0.8,
			offset=offset,
			number=request_count
			)

		print("Retrieved " + str(len(response.sources)) + " source name. Offset: " + str(offset) + "/" + str(max_results) +
			  ". Total available: " + str(response.available) + ".")

		if len(response.sources) == 0:
			break

		all_results.extend(response.sources)
		offset += 100

except worldnewsapi.ApiException as e:
	print("Exception when calling NewsApi->search_news: %s\n" % e)


for article in all_results:
    print("\nTitle: " + str(article.title))
    print("Author: " + str(article.authors))
    print("URL: " + str(article.url))
    print("Sentiment: " + str(article.sentiment))
    print("Text: " + str(article.text[:80]) + "...") # print first 80 characters of the text