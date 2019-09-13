#!/usr/bin/env python3
import json
import os
import time
from urllib.request import urlretrieve
from urllib.parse import urlparse
import urllib

import re
import requests
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Waypoint 1: Write a Python Class Episode
class Episode:
    def __init__(self, title, page_url, image_url, broadcasting_date ):
        """
            @params: title: the title of Episode class (read only).
                     page_url: URL of the web page dedicated to this Episode
                     (read only).
                     image_url: URL of the image (read only).
                     broadcasting_date: The date when this Episode
                                       has been broadcast (read only).
            @return: object Episode (print all parameters).
        """
        self.__title = title
        self.__page_url = "http://www.tv5monde.com" + page_url
        self.__image_url = image_url
        self.__broadcasting_date = broadcasting_date

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

    @staticmethod
    def from_json(payload):
        title = payload['title']
        page_url = payload['url']
        image_url = payload['image']
        broadcasting_date = payload['date']
        template_class = Episode(title, page_url, image_url, broadcasting_date)
        template_class.duration = payload['duration']
        return template_class



# Waypoint 2: Retrieve the Identification of an Episode
    @staticmethod
    def __parse_episode_id(url):
        """
            @params: staticmethod __parse_episode_id representing
                     the Uniform Resource Locator of the image of an episode
                     property episode_id is __parse_episode_id (read only)
            @return: the indentification of the Episode (a string)
                     the indentification of the Episode
        """
        file_name = os.path.basename(url)
        file_name_without_extension, file_extension = os.path.splitext(file_name)
        return file_name_without_extension


    @property
    def episode_id(self):
        self.__episode_id = self.__parse_episode_id(self.__image_url)
        return self.__episode_id

# TEST WP1
# with open('./merci-professeur.json', 'r') as myfile:
#     data = myfile.read()# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
# episodes = fetch_episodes(url)
# episode = episodes[0]
# # download all videos and save to folder Music
# print(download_episode_video_segments(episode, path='~/Music'))
# payload = json.loads(data)
# payload_0 = payload['episodes'][0]
# episode = Episode.from_json(payload_0)
# print(episode.title)
# print (episode.page_url)
# print (episode.image_url)
# print (episode.broadcasting_date)
# print(episode.duration)
# episode.title = 'sth else'
# print(episode.title)

# TEST WP2
# print (episode.episode_id)


# Waypoint 3: Fetch the List of Episodes
def read_url(
        url,
        maximum_attempt_count=3,
        sleep_duration_between_attempts=10):
    """
        @params: except is the sleep time when the program Connection Error.
                 read_url function use to edit issues such as: network, machine,
                                                                   application.
                 argument url (string)  that performs the HTTP request to the
                                            specified endpoint.
        @return: a list of objects Episode
                 read_url function returns the data read contained in the HTTP
                 response.

    """
    attempt_count = 0
    while attempt_count < maximum_attempt_count:
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
            attempt_count += 1

        # Waypoint 5: when read html_page return json so the function raise
        # ValueError of the html_content, converts return to text (string) for wp5
        except ValueError:
            return response.text
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
# print(read_url(url))


# Waypoint 4: Fetch the List of all the Episodes (update function from waypoint3)
def fetch_episodes(url):
    """
        @params: fetch_episodes allows to get the list of episodes.
                 url: receive the url http://
        @returns: returns a page of episodes.
    """

    # get the number of pages
    numPages = read_url(url)["numPages"]

    # list to contain objects Episode
    list_episodes = []

    for i in range(1,numPages+1,1):

        # format url for page
        final_url_string = url + "?page={}".format(i)

        # get json data from url
        data = read_url(final_url_string)

        # get each episode's json data
        for episode in data['episodes']:

            # append to list
            list_episodes.append(Episode.from_json(episode))
    return list_episodes

# TEST WP3, WP4
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
# episodes = fetch_episodes(url)
# for episode in episodes:
#     print(episode.page_url)


# Waypoint 5: Parse Broadcast Data of an Episode
# Fetch the HTML source page of the episodeP1
def fetch_episode_html_page(episode):
    """
        @param: episode calls the function read_url to read data (bytes)
                from the specified URL, and converts these data
                (encoded in UTF-8) to a string
        @returns: the textual HTML content of the episode page
                  the scheme, the hostname, the path starts with i//hls,
                  the TS file name starts with segment, the query.
    """
    html_content = read_url(episode.page_url)
    return html_content

# Parse broadcast information about the episode's video
def parse_broadcast_data_attribute(html_page):
    """
        @param: html_page takes an argument html_page, a string corresponding
                to the source code of the HTML page of an episode.
        @returns: a JSON expression corresponding to the string value of
                  the attribute data-broadcast.
    """
    # String processing using regex
    match_string = re.search(r"data-broadcast='([^']*)'", html_page)
    broadcast_data = match_string.group(1)
    return json.loads(broadcast_data)

# TEST WP5
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
# episodes = fetch_episodes(url)
# episode = episodes[0]
# episode_html_page = fetch_episode_html_page(episode)
# print(episode_html_page)
# print(len(episodes))
# print(parse_broadcast_data_attribute(episode_html_page))


# Waypoint 6: Build a URL Pattern of the Video Segments of an Episode
def build_segment_url_pattern(broadcast_data):
    """
        @param: broadcast_data representing the broadcast data of an episode
        @returns: a string representing a URL pattern that references
                  the video segments of this episode.
    """
    broadcast_url = broadcast_data['files'][0]['url']
# WP10:
    # if file format is mp4:
    broadcast_format = broadcast_data['files'][0]['format']
    if broadcast_format = 'mp4':
        segment_url = urlparse(broadcast_url)
        return segment_url.geturl()

    # if file format is m3u8
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


# Waypoint 7: Download the Video Segments of an Episodeeeeeeeeeeeeeee
def download_episode_video_segments(episode, path=None):
    """
        @param: episode that downloads all the TS video segments of this episode
        @returns: the absolute path and file names of these video segments
                  in the order of the segment indices.
    """
    try:
        # read the html page of episode
        episode_html_page = fetch_episode_html_page(episode)

        # get the json data of attribute data-broadcast from html page
        broadcast_data = parse_broadcast_data_attribute(episode_html_page)

        # build the sample segment pattern to download
        segment_pattern = build_segment_url_pattern(broadcast_data)

        # check if path is input
        if path is not None:
            path = os.path.expanduser(path)

            # check path exists if not create path
            if not os.path.isdir(path):
                os.mkdir(path)

        # if path is not input set path = current working directory
        else:
            path = os.getcwd()

        # segment index
        index = 1

        # list contain downloaded segments
        downloaded_videos = []

        # start the download loop
        while True:

            # format index of segment pattern to download
            segment_url = segment_pattern.format(index)

            # create segment file name if format is m3u8
            file_name = 'segment_{}_{}.ts'.format(episode.episode_id, index)

            # create segment file name if format is mp4
            if 'mp4' in segment_pattern:
                file_name = 'segment_{}_{}.mp4'.format(episode.episode_id, index)

            # create final file name to download
            des_path = path  + '/' + file_name

# Waypoint 9: Implement a Cache Strategy
            # if video segment already downloaded
            if os.path.exists(des_path):
                print(des_path + ' already downloaded')

            # if video segment not downloaded
            else:
                # download the segment
                urlretrieve(segment_url, des_path)

            # append to list
            downloaded_videos.append(des_path)

            # wp10
            if 'mp4' in segment_pattern:
                return downloaded_videos

            # update index value
            index += 1

    # when there's no more segments to download
    except urllib.error.HTTPError:
        return downloaded_videos

# TEST WP7
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
# episodes = fetch_episodes(url)
# episode = episodes[0]
# print(episode.title)
# print(eposode.episode_id)
# print(episode.page_url)
# segments = download_episode_video_segments(episode, path='~/Desktop')
# download in Home ~/ => Desktop, then after Desktop have /bla so create 1 folder
# print(segments)


# Waypoint 8: Build the Final Video of an Episode
def build_episode_video(episode, segment_file_path_names, path=None):
    """
        @param: episode An object Episode.
                segment_file_path_names a list of strings corresponding to
                absolute path and file names of TS video segments in
                the order of their index.
        @returns: the absolute path and file name of the episode's video.
    """

    # create file name
    file_name = episode.episode_id + '.ts'

    # wp10:
    if 'mp4' in segment_file_path_names[0]:
        file_name = episode.episode_id + '.mp4'

    # check if path is not input, set path = the directory contain first segment
    if path is None:
       path = os.path.dirname(segment_file_path_names[0])

    # get full input path
    path = os.path.expanduser(path)

    # if input path is not exists, create path
    if not os.path.exists(path):
        os.mkdir(path)

    # create final file name combine with path
    file_name = path + '/' + file_name

    # if video already combine
    if os.path.exists(file_name):
        return file_name

    # create the full video
    final_clip = concatenate_videoclips([VideoFileClip(segment) for segment \
    in segment_file_path_names])

    # write content of full video to file
    final_clip.write_videofile(file_name, codec = "libx264")
    return file_name


# TEST WP8
url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
episodes = fetch_episodes(url)
episode = episodes[0]
segment_file_path_names = download_episode_video_segments(episode, path='~/Small_videos')
file_name = build_episode_video(episode, segment_file_path_names, path='~/Big_video')
print(file_name)
