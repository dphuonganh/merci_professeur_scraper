#!/usr/bin/env python3
import json
import os
import time
from urllib.request import urlretrieve
from urllib.parse import urlparse
import urllib

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
            payload['date'],
            payload['duration'])

# Waypoint 2: Retrieve the Identification of an Episode
    @staticmethod
    def __parse_episode_id(url):
        file_name = os.path.basename(url)
        file_name_without_extension, file_extension = os.path.splitext(file_name)
        return file_name_without_extension

    @property
    def episode_id(self):
        if self.__episode_id is None:
            self.__episode_id = self.__parse_episode_id(self.__image_url)
        return self.__episode_id

# TEST WP1
# with open('./merci-professeur.json', 'r') as myfile:
#     data = myfile.read()
# payload = json.loads(data)
# payload_0 = payload['episodes'][0]
# episode = Episode.from_json(payload_0)
# print (episode.title)
# print (episode.page_url)
# print (episode.image_url)
# print (episode.broadcasting_date)
# print (episode.duration)
# episode.title = 'sth else'

# TEST WP2
# print (episode.episode_id)


# Waypoint 3: Fetch the List of Episodes
def read_url(
        url,
        maximum_attempt_count=3,
        sleep_duration_between_attempts=10):
    while True:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0)\
            Gecko/20100101 Firefox/46.0'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()

            raise Exception('Resource not found/not allowed')

        except requests.exceptions.ConnectionError:
            print("Toi ngu mot chut...")
            time.sleep(sleep_duration_between_attempts)
            print("Toi thuc day")

        except ValueError:
            return response.text


# Waypoint 4: Fetch the List of all the Episodes (update function from waypoint 3)
def fetch_episodes(url):
    numPages = read_url(url)["numPages"]
    list_episodes = []
    for i in range(1,numPages+1,1):
        final_url_string = url + "?page={}".format(i)
        data = read_url(final_url_string)
        for episode in data['episodes']:
            list_episodes.append(Episode.from_json(episode))
    return list_episodes

# TEST WP3, WP4
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
# episodes = fetch_episodes(url)
# for episode in episodes:
#     print(episode.page_url)


# Waypoint 5: Parse Broadcast Data of an Episode
# Fetch the HTML source page of the episode
def fetch_episode_html_page(episode):
    html_content = read_url(episode.page_url)
    return html_content

# Parse broadcast information about the episode's video
def parse_broadcast_data_attribute(html_page):
    # String processing
    broadcast_line = [line for line in html_page.split('\n') if \
    'data-broadcast' in line]
    broadcast_line = broadcast_line[0].split("data-broadcast=\'")[1]
    broadcast_attribute = broadcast_line.split("\' data-duration")[0]
    return json.loads(broadcast_attribute)

# TEST WP5
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
# episodes = fetch_episodes(url)
# episode = episodes[0]
# episode_html_page = fetch_episode_html_page(episode)
# print(len(episodes))
# print(episode_html_page)
# print(parse_broadcast_data_attribute(episode_html_page))


# Waypoint 6: Build a URL Pattern of the Video Segments of an Episode
def build_segment_url_pattern(broadcast_data):
    broadcast_url = broadcast_data['files'][0]['url']
    head, sep, tail = broadcast_url.partition('csmil/')
    segment_url = urlparse(head + sep + 'segment{}_3_av.ts?null=0')
    return segment_url.geturl()

# TEST WP6
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
# episodes = fetch_episodes(url)
# episode = episodes[0]
# episode_html_page = fetch_episode_html_page(episode)
# broadcast_data = parse_broadcast_data_attribute(episode_html_page)
# print(broadcast_data)
# segment_url_pattern = build_segment_url_pattern(broadcast_data)
# print('\n' + segment_url_pattern + '\n')
# print(segment_url_pattern.format('1'))


# Waypoint 7: Download the Video Segments of an Episode
def download_episode_video_segments(episode, path=None):
    try:
        episode_html_page = fetch_episode_html_page(episode)
        broadcast_data = parse_broadcast_data_attribute(episode_html_page)
        index = 1
        response = 0
        downloaded_videos = []
        while response != 404:
            segment_url=build_segment_url_pattern(broadcast_data).format(index)
            file_name = 'segment_{}_{}.ts'.format(episode.episode_id, index)
            response = requests.get(segment_url).status_code
            urlretrieve(segment_url, file_name)
            if path is not None:
                des_path = os.path.expanduser(path) + '/' + file_name
                os.rename(file_name, des_path)
                downloaded_videos.append(des_path)
            else:
                downloaded_videos.append(os.getcwd() + '/' + file_name)
            index += 1
    except urllib.error.HTTPError:
        return downloaded_videos

# TEST WP7
url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
episodes = fetch_episodes(url)
episode = episodes[0]
# download all videos and save to folder Music
print(download_episode_video_segments(episode, path='~/Music'))


# Waypoint 8: Build the Final Video of an Episode
def build_episode_video(episode, segment_file_path_names, path=None):
    pass
