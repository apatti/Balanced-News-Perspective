import json
from agno.tools.googlesearch import GoogleSearchTools
from duckduckgo_search import DDGS

class Extractor:
    def __init__(self,max_results=3):
        self.__fixed_max_results = max_results
        self.__googleUtil = GoogleSearchTools(
            fixed_max_results=max_results,
            fixed_language="en",
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})
        
        self.__duckUtil = DDGS()

    def __getGoogleNews(self, query) -> list[str]:
        assert query, "Query is mandatory"
        response = json.loads(self.__googleUtil.google_search(f"-site:youtube.com {query}"))
        return [result["url"] for result in response 
                    if "video" not in result["url"] or 
                        "tag" not in result["url"] or 
                        "google.com/search" not in result["url"]]

    def __getNewsDDG(self, query) -> list[str]:
        assert query, "Query is mandatory"
        response = self.__duckUtil.news(keywords=f"{query}", max_results=self.__fixed_max_results)
        return [result["url"] for result in response if "video" not in result["url"]]

    def getNewsUrls(self, query) -> list[str]:
        googleNews = self.__getGoogleNews(query)
        duckNews = self.__getNewsDDG(query)
        return list(set(googleNews + duckNews))

if __name__ == "__main__":
    extractor = Extractor(max_results=15)
    print(extractor.getNewsUrls("musk federal firing"))