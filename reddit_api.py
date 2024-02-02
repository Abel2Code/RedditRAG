import requests
import json
from retry import retry
from joblib import Memory
memory = Memory("cache")

@retry(tries=5, delay=5)
def __query_json_url__(url):
    print(url)
    res = requests.get(url)    
    assert res.status_code == 200, res.status_code
    return res.json()

@memory.cache
def fetch_top_reddit_comment(keywords, subreddit):
    keywords = '%20'.join(keywords)
    
    search_url = "https://www.reddit.com/{}/search.json?restrict_sr=1&limit=1&q={}".format(subreddit, keywords)
    
    permalink = __query_json_url__(search_url)['data']['children'][0]['data']['permalink']
    
    post_url = f"https://www.reddit.com{permalink[:-1]}.json?limit=5"

    res = __query_json_url__(post_url)

    comments = res[1]['data']['children'][:5]
    comments = [c['data']['body'] for c in comments if 'body' in c['data'] and c['data'].get("distinguished", None) != 'moderator']
    
    return comments