from youtube_search import YoutubeSearch
import json

class UrlFetcher:
  def getUrl(keyword):
    print(keyword)
    results = YoutubeSearch(keyword, max_results=1).to_json()
    jsonObject = json.loads(results)
    resolvedUrl = "https://www.youtube.com" + jsonObject['videos'][0]['url_suffix']
    print("received keyword:", keyword, "resovled url: ", resolvedUrl)
    return resolvedUrl

# https://pypi.org/project/youtube-search/

#https://www.youtube.com/watch?v=89dGC8de0CA

