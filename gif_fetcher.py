import pprint

import requests
from PIL import Image
from io import BytesIO

ENV = "test"


class GifFetcher:

    def __init__(self, env: str):
        self.env = env
        self.api_key = self.read_api_key()

    def read_api_key(self) -> str:
        base_path = "./SECRETS/{env}/giffy_api_key"

        env_path = base_path.format(env=self.env)

        with open(env_path) as f:
            giffy_api_key = f.read().strip()

        return giffy_api_key

    def get_trending(self, limit: int = 20, offset: int = 0):

        trending_url = "http://api.giphy.com/v1/gifs/trending"
        payload = {
            'api_key': self.api_key,
            'limit': limit,
            'offset': offset,
            'rating': 'pg-13',  # no R rated gifs please
        }
        r = requests.get(trending_url, params=payload)

        pp = pprint.PrettyPrinter()
        pp.pprint(r.json())

        # todo: add retries for flakey responses
        assert(r.status_code == 200)

        image_infos = r.json()['data']
        for image_info in image_infos:
            filename = image_info.get('id')
            url = image_info['images']['original']['url']
            self.save_raw_image(url=url, filename=filename)

        count_received = r.json()['pagination']['count']
        count_left = r.json()['pagination']['total_count']
        if count_received < limit and count_left > 0:
            limit -= count_received
            offset += count_received

            self.get_trending(limit, offset)

    @staticmethod
    def save_raw_image(url: str, filename: str):
        r = requests.get(url=url)
        i = Image.open(BytesIO(r.content))

        i.save(f"./img/{filename}.gif", save_all=True)


# todo: turn this into proper command line args
gf = GifFetcher(env='test')
gf.get_trending(limit=200, offset=0)

