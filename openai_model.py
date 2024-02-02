import os

from openai import OpenAI
from retry import retry
from dotenv import load_dotenv

from helper import update_cache, load_cache

load_dotenv()

api_key = os.getenv("OPEN_AI_KEY")
client = OpenAI(api_key=api_key)

class OpenAI_Model():
    def __init__(self, cache_path='./cache.json'):
        self.cache_path = cache_path
        self.cache = load_cache(cache_path)

    def __call_openai_api__(self, prompt):
        return client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
        ).choices[0].message.content

    @retry(tries=1)
    def query(self, prompt, parser=lambda x: x):
        assert isinstance(prompt, str)

        if prompt in self.cache:
            return self.cache[prompt]
        
        res = self.__call_openai_api__(prompt)

        res = parser(res)        
        
        self.cache[prompt] = res
        return res
              
    def save_cache(self):
        update_cache(self.cache_path, self.cache)