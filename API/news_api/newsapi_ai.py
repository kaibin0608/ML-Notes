from eventregistry import EventRegistry, QueryArticlesIter, QueryItems
# since we want recent results, just prevent use of archive - in this way we don't need to set any date constraints

API_KEY = "5ff63ede-ac37-47f4-b8c3-ab2ebaece1ab"

er = EventRegistry(apiKey = API_KEY, allowUseOfArchive = False)


def run_search_news_api(
                keywords, 
                starting_date,
                ending_date, 
                max_results=100):
    
    q = QueryArticlesIter(
        keywords = QueryItems.OR(keywords),
        # lang=QueryItems.OR(["eng",]),
        sourceLocationUri="http://en.wikipedia.org/wiki/Malaysia",
        dateStart=starting_date,
        dateEnd=ending_date,
        keywordsLoc = "body,title",
        keywordSearchMode = "exact",
        isDuplicateFilter="skipDuplicates",
        hasDuplicateFilter="skipHasDuplicates",
        dataType= ["news", "pr"],
        )

    # we limit here the results to 100. If you want more, remove or increasae maxItems
    for article in q.execQuery(er, sortBy="date", sortByAsc=False, maxItems=max_results):
        print(article)

# Alternative way using complex query
# er = EventRegistry(apiKey = API_KEY)
# query = {
#   "$query": {
#     "$and": [
#       {
#         "keyword": {"$or":["SSM", "大马公司委员会"]},
#         "keywordSearchMode": "exact"
#       },
#       {
#         "sourceLocationUri": "http://en.wikipedia.org/wiki/Malaysia"
#       },
#       {
#         "dateStart": "2025-09-18",
#         "dateEnd": "2025-10-31"
#       }
#     ]
# #   },
# #   "$filter": {
# #     "forceMaxDataTimeWindow": "31"
#   }
# }
# q = QueryArticlesIter.initWithComplexQuery(query)
# # change maxItems to get the number of results that you want
# for article in q.execQuery(er, maxItems=100):
#     print(article)

if __name__ == "__main__":
    keywords = ["Akta Syarikat 2016"]
    starting_date = "2025-10-18"
    ending_date = "2025-10-31"
    run_search_news_api(
        keywords,
        starting_date,
        ending_date,
        max_results=100
    )
                