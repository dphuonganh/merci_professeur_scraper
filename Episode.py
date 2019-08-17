import json;
# Waypoint 1: Write a Python Class Episode
class Episode: # _ co the gan duoc luc test print title = "a"
    def __init__(self, title, page_url, image_url, broadcasting_date, duration):
        self._title = title
        self._page_url = "http://www.tv5monde.com" + page_url
        self._image_url = image_url
        self._broadcasting_date = broadcasting_date
        self._duration = duration

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
    def _duration(self):
        return self._duration

    @staticmethod
    def from_json(payload):
        return Episode(payload["title"], payload["url"], payload["image"], payload["date"], payload["duration"])

payload = {
    "title": "Valeurs républicaines",
    "url": "/emissions/episode/merci-professeur-valeurs-republicaines",
    "image": "https://vodhdimg.tv5monde.com/tv5mondeplus/images/4832517.jpg",
    "date": "Mardi 13 août 2019 (redif. du Jeudi 30 novembre 2017)",
    "duration": "01:49"
}

a = Episode.from_json(payload)
# Waypoint 2: Retrieve the Identification of an Episode
