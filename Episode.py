import json
import requests

# Waypoint 1: Write a Python Class Episode
class Episode: # _ co the gan duoc luc test print title = "a"
    def __init__(self, title, page_url, image_url, broadcasting_date, duration):
        self._title = title
        self._page_url = "http://www.tv5monde.com" + page_url
        self._image_url = image_url
        self._broadcasting_date = broadcasting_date
        self._duration = duration
        self._episode_id = None

    @property
    def title(self):
        return self._title

    @property
    def page_url(self):
        return self._page_url

    @property
    def image_url(self):
        return self._image_url

    @property
    def broadcasting_date(self):
        return self._broadcasting_date

    @property
    def duration(self):
        return self._duration

    @staticmethod
    def from_json(payload):
        return Episode(payload['title'], payload["url"], payload["image"],\
        payload["date"], payload["duration"])

# Waypoint 2: Retrieve the Identification of an Episode
    @staticmethod
    def __parse_episode_id(url):
        return url.split('.')[2].split('/')[3]

    @property
    def episode_id(self):
        self._episode_id = self.__parse_episode_id(self._image_url)
        return self._episode_id

with open('./merci-professeur.json', 'r') as myfile:
    data = myfile.read()
payload = json.loads(data)
payload_0 = payload['episodes'][0]
a = Episode.from_json(payload_0)
# TEST WP1
# print (a.title)
# print (a.page_url)
# print (a.image_url)
# print (a.broadcasting_date)
# print (a.duration)
# a.title = 'sth else'
# print (a.title)

# TEST WP2
# print (a.episode_id)


# Waypoint 3: Fetch the List of Episodes
def read_url(url, maximum_attempt_count=3,
    sleep_duration_between_attempts=10):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0)\
    Gecko/20100101 Firefox/46.0'}
    r = requests.get(url, headers=headers)
    return r.json()


def fetch_episodes(url):
    return (read_url(url))


url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
print(fetch_episodes(url))
