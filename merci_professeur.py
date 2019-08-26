import json
import os
import time

import requests

# Waypoint 1: Write a Python Class Episode
class Episode: # _ co the gan duoc luc test print title = "a"
    def __init__(self, title, page_url, image_url, broadcasting_date, duration):
        self.__title = title
        self.__page_url = "http://www.tv5monde.com" + page_url
        self.__image_url = image_url
        self.__broadcasting_date = broadcasting_date
        self.__duration = duration
        self.__episode_id = None

    @property
    def title(self):
        return self.__title

    @property
    def page_url(self):
        return self.__page_url

    @property
    def image_url(self):
        return self.__image_url

    @property
    def broadcasting_date(self):
        return self.__broadcasting_date

    @property
    def duration(self):
        return self.__duration

    @staticmethod
    def from_json(payload):
        return payload and Episode(
            payload['title'],
            payload['url'],
            payload['image'],
            payload['date'],  raise Exception('Resource not found/not allowed')

        except requests.exceptions.ConnectionError:
            time.sleep(sleep_duration_between_attempts)
            payload['duration'])

# Waypoint 2: Retrieve the Identification of an Episode
    @staticmethod
    def __parse_episode_id(url):
        print(url)
        file_name = os.path.basename(url)
        file_name_without_extension, file_extension = os.path.splitext(file_name)
        return file_name_without_extension

    @property
    def episode_id(self):
        if self.__episode_id is None:
            self.__episode_id = self.__parse_episode_id(self.__image_url)
        return self.__episode_id




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
def read_url(
        url,
        maximum_attempt_count=3,
        sleep_duration_between_attempts=10):
    while True:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0)\
            Gecko/20100101 Firefox/46.0'}
            request = requests.get(url, headers=headers)
            if request.status_code == 200:
                return request.json()

            raise Exception('Resource not found/not allowed')

        except requests.exceptions.ConnectionError:
            print("Toi ngu mot chut...")
            time.sleep(sleep_duration_between_attempts)
            print("Toi thuc day")



def fetch_episodes(url):
    data = read_url(url)
    list_episodes = []
    for episode in data['episodes']:
        list_episodes.append(Episode.from_json(episode))
    return list_episodes

episodes = fetch_episodes('http://www.tv5monde.com/emissions/episodes/merci-professeur.json')


url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
list_episodes = fetch_episodes(url)
for episode in list_episodes:
    print(episode.episode_id)

 requests.get('http://majormode.com/fake')