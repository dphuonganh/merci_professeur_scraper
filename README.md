# "Merci professeur !" Episode Video Scraper

![merci_professeur_program](/merci_professeur_program.jpg)

["Merci professeur !"](http://www.tv5monde.com/emissions/episodes/merci-professeur) is a short linguistic program presented by Bernard CERQUIGLINI on TV5MONDE, the world's leading French-language cultural broadcaster that reaches more than 318 million households and 32 million viewers every week in 200 countries and territories:

![tv5monde](/tv5monde.png)

Each episode of this program presents, with humor and simplicity, and in less than 2 minutes, linguistic, etymological, orthographic, and grammatical difficulties of the French language. Viewers can ask Bernard CERQUIGLINI questions about the French language's subtleties which answer will be directly broadcast.

"Merci professeur !" is probably the most accessible and interesting program about the French language. There are hundreds of episodes available on the Internet. However, these episodes are not greatly highlighted on TV5MONDE web site, while they could be integrated in a free mobile application that would push a new episode to the subscribers, for instance, every morning, to enjoy with a coffee and croissants. :)

Your mission, should you choose to accept it, is to find a way to hack TV5MONDE Web site's data, to download and rebuild the episode videos. As always, should you be caught, the Secretary will disavow any knowledge of your actions. Good luck.

![impossible_mission_wallpaper](/impossible_mission_wallpaper.jpg)

# Waypoint 1: Write a Python Class Episode

We have started to hack TV5MONDE Web site's data and we have discovered that it is using a private API to fetch the list of the episodes that are displayed.

The URL of this endpoint is: http://www.tv5monde.com/emissions/episodes/merci-professeur.json.

This endpoint returns a JSON expression that contains an array of dictionaries, each dictionary corresponds to the information of an episode. We can discover the structure of the response returned by this API's endpoint with the following Shell command:

> curl --silent http://www.tv5monde.com/emissions/episodes/merci-professeur.json | json_pp|

We will store the information of an episode in an object.

Write a [Python class](https://www.youtube.com/watch?v=ZDa-Z5JzLYM) `Episode` which constructor takes the following parameters in that particular order:



* `title`: The title of the episode

* `page_url`: The Uniform Resource Locator (URL) of the Web page dedicated to this episode

* `image_url`: The Uniform Resource Locator (URL) of the image (poster) that is shown while the video of the episode is downloading or until the user hits the play button; this is the representative of the episode's video

* `broadcasting_date`: The date when this episode has been broadcast


Write a [static method](https://realpython.com/instance-class-and-static-methods-demystified/) `from_json` of this [class](https://www.youtube.com/watch?v=apACNr7DC_s) that takes an argument `payload` (a JSON expression) and that returns an object `Episode`.

The class `Episode`'s attributes **MUST** be [private](https://docs.python.org/3.7/tutorial/classes.html#tut-private). They **MUST** be accessible through the [read-only properties](https://www.youtube.com/watch?v=jCzT9XFZ5bw) `title`, `page_url`, `image_url`, and `broadcasting_date`.

Also, the private attribute page_url, corresponding to the URL of the episode's Web page, MUST start with the string "`http://www.tv5monde.com`".

# Waypoint 2: Retrieve the Identification of an Episode(https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent)

Each episode is identified with a number.

We have discovered that this identification can be extracted from the URL of the representative image of the episode's video (cf. `image_url`). The file of this image is actually named after the identification of the episode.

For example:

> https://vodhdimg.tv5monde.com/tv5mondeplus/images/5022428.jpg


The identification of this episode is 5022428.

You need to:


1. Add a private [static method](https://realpython.com/lessons/regular-instance-methods-vs-class-methods-vs-static-methods/) `__parse_episode_id` to the class `Episode` that takes an argument `url` (a string) representing the Uniform Resource Locator of the image of an episode, and that returns the identification of the episode (a string);

2. Update the constructor of the class `Episode` to create an additional private attribute and set its value with the identification of the episode extracted from the URL of the representative image of the episode;

3. Add a read-only [property](https://www.programiz.com/python-programming/property) `episode_id` to the class `Episode` that returns the identification of the episode.

# Waypoint 3: Fetch the List of Episodes

Now that we have a class `Episode`, we can easily instantiate objects by providing JSON expressions representing episodes.

You will need to write a function `fetch_episodes` that takes an argument `url` (a string) that corresponds to the Uniform Resource Locator (URL) of the TV5MONDE's endpoint which allows to get the list of episodes.

The function sends a HTTP `GET` request to the specified TV5MONDE's private API, reads the JSON data returned by this endpoint, and returns a list of objects `Episode`.

There are a few points you need to consider that we present hereafter.

# Permanent and Temporary Errors Management

When connecting to a machine through the Internet, and sending and retrieving data to and from a remote machine, your definitively **MUST** expect to face a couple of issues:


* network issue: your machine or the remote machine is not currently connected to the Internet, the remote machine is not accessible because of various possible failures between your machine and this remote machine (DNS, router, firewall, switch, etc.);

* machine issue: the remote machine is down, its network interface is down, etc.

* application issue: the Web sever application of this machine is down or it is not responding, the resource specified in your HTTP request does not exist or its access is not allowed, etc.


You **MUST** distinguish permanent errors (resource is [not found](https://en.wikipedia.org/wiki/HTTP_404), its access is [not forbidden](https://en.wikipedia.org/wiki/HTTP_403), etc.), from temporary errors (connectivity issue, [server](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#5xx_Server_errors) issues). Temporary errors are recoverable. Permanent errors are not. In case of temporary errors, your code SHOULD try to reattempt the same request some times later.

**Separation of Concerns (SoC)**

You **SHOULD** definitively write the code that handles the HTTP request to the endpoint specified by an in a separate function. This is the [Separation of Concerns (SoC)](https://en.wikipedia.org/wiki/Separation_of_concerns) principle: each function addresses on one and only one concern. This principle allows better modularity and maintainability of your code.

You **SHOULD** write a function `read_url` that takes an argument `url` (a string), that performs the HTTP request to the specified endpoint, and that returns the data read contained in the HTTP response. This function **SHOULD** reattempts a certain number of times to connect and read data from the specified URL when temporary errors occur.

Your function `fetch_episodes` calls this other function `read_url` to read the JSON expression representing a list of episodes fetched from the TV5MONDE's private API.

**Spoofing Browser Identity**

Your application needs to disguise itself, i.e., to fake a browser application that impersonates a real user. Why? Because some Web servers don't allow client applications other than browsers to fetch data from their private API. How do they recognize browsers. They read a special HTTP header, `[User-Agent]`(https://en.wikipedia.org/wiki/User_agent), from the HTTP request they received. If the HTTP header `User-Agent` doesn't reference an accepted browser, the Web server may deny the access to the requested resource.

Your function `read_data_from_url` needs to add an HTTP header `[User-Agent]`(https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent) with a real browser identification when your function sends the HTTP request to TV5MONDE private API.

**Waypoint 4: Fetch the List of all the Episodes

TV5MONDE's private API doesn't return all the episodes available online in only one request. It only returns a page of episodes.

How to fetch all the episodes? TV5MONDE's private API supports [pagination](https://www.moesif.com/blog/technical/api-design/REST-API-Design-Filtering-Sorting-and-Pagination/#). You may have noticed that the JSON expression, returned by TV5MONDE private API, contains an attribute `numPages` that indicates the number of pages.

The endpoint of this API supports a query parameter `page` that allows the caller to indicate the index of the page to return episodes from. This index starts with `1`. By default, when not defined, the page index value is `1`.

For example:

> curl --silent http://www.tv5monde.com/emissions/episodes/merci-professeur.json?page=2 | json_pp

Update your function `fetch_episodes` to return all available episodes.

**Waypoint 5: Parse Broadcast Data of an Episode

We need now to understand how the [video of an episode](http://www.tv5monde.com/emissions/episode/merci-professeur-kilometre-par-heure) is downloaded by your browser and how it is played.

For that you need to open the [page of an episode](http://www.tv5monde.com/emissions/), to click on the [High Definition (HD) video option](https://en.wikipedia.org/wiki/High-definition_video), and to inspect network activity between your browser and TV5MONDE Web site.

**Developer Tools: Network Activity

You need to access the Developer Tools of your browser. Most of the browsers, such as [Chrome](https://developers.google.com/web/tools/chrome-devtools/) and [FireFox](https://developer.mozilla.org/en-US/docs/Tools), support a set of tools that help developers edit pages on-the-fly and diagnose problems quickly.

For example, with Google Chrome, the developer Web Tool provides a tab to access [network activity](https://www.youtube.com/watch?time_continue=6&v=e1gAyQuIFQo).

You can filter resources that the browser accesses to by entering some keywords. Enter the keyword `segment`. You will see a list of TS files such as `segment1_3_av.ts?null=0`, `segment2_3_av.ts?null=0`, etc.:

![browser_network_analysis.gif](đường dẫn)

[Transport Stream (TS)](https://en.wikipedia.org/wiki/MPEG_transport_stream) is a standard format specified in MPEG-2 for the transmission and storage of audio, video and data, and commonly used in broadcast systems.

If you click on one particular TS files displayed in the filtered list, you have access to detailed information about this resource, such as its location referenced by the request URL, for example:

> https://hlstv5mplus-vh.akamaihd.net/i/hls/61/5022428_,300,700,1400,2100,k.mp4.csmil/segment1_3_av.ts?null=0
>
> We can manually download this file to watch it:
>
>  Download the video file "segment1_3_av.ts".
> $ wget --output-document=segment1_3_av.ts "https://hlstv5mplus-vh.akamaihd.net/i/hls/61/5022428_,300,700,1400,2100,k.mp4.csmil/segment1_3_av.ts?null=0"
--2019-08-08 11:22:04--  https://hlstv5mplus-vh.akamaihd.net/i/hls/61/5022428_,300,700,1400,2100,k.mp4.csmil/segment1_3_av.ts?null=0
Resolving hlstv5mplus-vh.akamaihd.net (hlstv5mplus-vh.akamaihd.net)... 113.171.230.8
Connecting to hlstv5mplus-vh.akamaihd.net (hlstv5mplus-vh.akamaihd.net)|113.171.230.8|:443... connected.
HTTP request sent, awaiting response... 200 OK
> Length: 3165732 (3.0M) [video/MP2T]
> Saving to: ‘segment1_3_av.ts’
>
> segment1_3_av.ts          100%[==================================>]   3.02M  5.87MB/s    in 0.5s
>
> 2019-08-08 11:22:05 (5.87 MB/s) - ‘segment1_3_av.ts’ saved [3165732/3165732]
>  Display information about this file.
> $ ls -la segment1_3_av.ts
> -rw-r--r--@ 1 lythanhphu  student  3165732 Aug  8 11:22 segment1_3_av.ts

You can watch this file with your favorite video reader, such as [VLC media player](https://www.videolan.org/vlc/index.html), a free and open source cross-platform multimedia player. You will then notice that this video is only the first 10 seconds of the episode.

**Video Segments

An episode is actually composed of a list of small TS videos (a [playlist](https://en.wikipedia.org/wiki/M3U)) to be played sequentially. This technique allows a kind of [progressive downloading](https://en.wikipedia.org/wiki/Progressive_download): the user can start to play the episode while the whole video is not completely downloaded.

You may have noticed that the TS videos are not hosted on TV5MONDE (`tv5monde.com`), but on another location (`akamaihd.net`). For instance `hlstv5mplus-vh.akamaihd.net`. These videos are actually hosted on [Akamai](https://en.wikipedia.org/wiki/Akamai_Technologies), a [Content Delivery Network (CDN)](https://en.wikipedia.org/wiki/Content_delivery_network).

Our scraper application will need to download the videos of an episode from Akamai's servers. But what is the URL of each TS segment?

If you watch several episodes and you inspect the network activity, you will find a common pattern of the request URL:


* `https://hlstv5mplus-vh.akamaihd.net/i/hls/61/5022428_,300,700,1400,2100,k.mp4.csmil/segment1_3_av.ts?null=0`
* `https://hlstv5mplus-vh.akamaihd.net/i/hls/73/5257520_,300,700,1400,2100,k.mp4.csmil/segment1_3_av.ts?null=0`
* `https://hlstv5mplus-vh.akamaihd.net/i/hls/9e/4927553_,300,700,1400,2100,k.mp4.csmil/segment1_3_av.ts?null=0`
* `https://hlstv5mplus-vh.akamaihd.net/i/hls/2b/5257518_,300,700,1400,2100,k.mp4.csmil/segment1_3_av.ts?null=0`


The common pattern between the request [URL](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier#Generic_syntax) to download these TS videos is:


* the **scheme** is `HTTPS`

* the **hostname** is `hlstv5mplus-vh.akamaihd.net`

* the **path** starts with `/i/hls`, followed with a magic number (for instance `2b`), followed with the episode identifier, followed with `_,300,700,1400,2100,k.mp4.csmil`

* the TS file name starts with `segment`, followed with the index of the video segment (starting with `1`), followed with `_3_av.ts`

* the query is `null=0`



We have discovered that the magic number is always the same for the video segments of a same episode, however this magic number is different from one episode to another. So how could we determine the magic number for a specific episode? What is the root file where we should expect to find it? More likely the episode HTML source page itself!

For example:

![html_page_source_01 (1).png](html_page_source_03.png)

You **SHOULD** search for the hostname `hlstv5mplus-vh.akamaihd.net`. You will find it is included in a JSON expression similar to: ...

Can you see the *magic number* there? Can you actually figure out how you can reuse the given URL to retrieve the video segments of this episode? [Can you see the light](https://www.youtube.com/watch?v=xbq0OuJtErs&feature=youtu.be&t=258)?!

*Hint: Nope?! Don't you see the similarity between the URL of the video segments of the episode and the URL that you can extract from the page source of this episode?*

> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment1_3_av.ts?null=0

and:

> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/master.m3u8

Write a function `fetch_episode_html_page` that takes an argument `episode` (an object `Episode`), and that returns the textual HTML content of the episode page (cf. `page_url`). This function internally calls the function `read_url` to read data (bytes) from the specified URL, and converts these data (encoded in UTF-8) to a string:

Write a function` parse_broadcast_data_attribute` that takes an argument `html_page`, a string corresponding to the source code of the HTML page of an episode, and that returns a JSON expression corresponding to the string value of the attribute `data-broadcast`.

For example:

>  Fetch the list of episodes.
> >>> episodes = fetch_episodes('http://www.tv5monde.com/emissions/episodes/merci-professeur.json?page={}')
> >>> len(episodes)
> 611
>  Fetch the HTML source page of the first episode of this list.
> >>> episode = episodes[0]
> >>> episode.page_url
> 'http://www.tv5monde.com/emissions/episode/merci-professeur-trace'
> >>> episode_html_page = fetch_episode_html_page(episode)
> '<!DOCTYPE html>\n<html lang="fr">\n<head>\n<meta charset="UTF-8" />\n...'
>  Parse broadcast information about the episode's video.
> >>> parse_broadcast_data_attribute(episode_html_page)
> {'files': [{'format': 'm3u8', 'url': 'https://hlstv5mplus- vh.akamaihd.net/i/hls/73/5257520_,300,700,1400,2100,k.mp4.csmil/master.m3u8'}], 'primary': 'html5', 'token': False}
  
**Waypoint 6: Build a URL Pattern of the Video Segments of an Episode

![mission_impossible_02.jpg]()

Using the URL provided in the broadcast data that we have extracted in the previous waypoint, we should be able to easily build an URL pattern for accessing the video segments of an episode.

We have inspected the network activity and we have seen that the URLs of the video segments of an episode are almost the same:

> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment1_3_av.ts?null=0
> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment2_3_av.ts?null=0
> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment3_3_av.ts?null=0
> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment4_3_av.ts?null=0
> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment5_3_av.ts?null=0
> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment6_3_av.ts?null=0
> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment7_3_av.ts?null=0
> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment8_3_av.ts?null=0
> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment9_3_av.ts?null=0
> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment10_3_av.ts?null=0
> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment11_3_av.ts?null=0
> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment12_3_av.ts?null=0
> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment13_3_av.ts?null=0
> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment14_3_av.ts?null=0
> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment15_3_av.ts?null=0
> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment16_3_av.ts?null=0

The only difference is that each URL of a video segment contains the index of this video segment, starting from 1. The URL pattern of the video segments of this particular episode is:

> https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/segment{}_3_av.ts?null=0

where `{}` could be easily replaced with the index of a video segment using the [string function 'format'](https://docs.python.org/3.7/library/stdtypes.html#str.format).

This URL pattern can be easily built from the broadcast data that our function `parse_broadcast_data_attribute` parses from the HTML source code of an episode, such as for example:

> https://hlstv5mplus-vh.akamaihd.net/i/hls/73/5257520_,300,700,1400,2100,k.mp4.csmil/master.m3u8

Write a function `build_segment_url_pattern` that takes an argument `broadcast_data` (a JSON expression), representing the broadcast data of an episode, and that returns a string representing a URL pattern that references the video segments of this episode.

For example:

>  Fetch the list of episodes.
> >>> episodes = fetch_episodes('http://www.tv5monde.com/emissions/episodes/merci-professeur.json?page={}')
> >>> len(episodes)
> 611
>  Fetch the HTML source page of the first episode of this list.
> >>> episode = episodes[0]
> >>> episode.page_url
> 'http://www.tv5monde.com/emissions/episode/merci-professeur-trace'
> >>> episode_html_page = fetch_episode_html_page(episode)
> '<!DOCTYPE html>\n<html lang="fr">\n<head>\n<meta charset="UTF-8" />\n...'
>  Parse broadcast information about the episode's video.
> >>> broadcast_data = parse_broadcast_data_attribute(episode_html_page)
> {'files': [{'format': 'm3u8', 'url': 'https://hlstv5mplus-vh.akamaihd.net/i/hls/73/5257520_,300,700,1400,2100,k.mp4.csmil/master.m3u8'}], 'primary': 'html5', 'token': False}
> >>> segment_url_pattern = build_segment_url_pattern(broadcast_data)
> >>> print(segment_url_pattern)
> https://hlstv5mplus-vh.akamaihd.net/i/hls/73/5257520_,300,700,1400,2100,k.mp4.csmil/segment{}_3_av.ts?null=0
>  Display the URL that references the first video segment.
> >>> print(segment_url_pattern.format('1'))
> https://hlstv5mplus-vh.akamaihd.net/i/hls/73/5257520_,300,700,1400,2100,k.mp4.csmil/segment1_

*Note*: you **SHOULD** use the [function `urlparse`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse) and the [class `ParseResult`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.ParseResult) to parse the URL provided in the broadcast data of the episode and to build the URL pattern.

**Waypoint 7: Download the Video Segments of an Episode

Write a function `download_episode_video_segments` that takes an argument `episode` (an object Episode), that downloads all the TS video segments of this episode, and returns the absolute path and file names of these video segments in the order of the segment indices.

The function `download_episode_video_segments` accepts an optional argument `path` (a string) that indicates in with directory the video segment files need to be saved into. If not defined, the function saves the video segment files in the current working directory.

The file name of each video segment **MUST** be composed with the following pattern:

> segment_{episode_id}_{segment_index}.ts'

where:

* episode_id: Identification of the episode

* segment_index: Index of the video segment

For example:

>  Let's consider the following episode:
> >>> episode
> <__main__.Episode object at 0x1052b2eb8>
> >>> episode.title
> 'Trace'
> >>> episode.episode_id
> '5257520'
> >>> episode.page_url
> 'http://www.tv5monde.com/emissions/episode/merci-professeur-trace'
>  Download all the video segments of this episode in our directory
>  "Movies".
> >>> download_episode_video_segments(episode, path='~/Movies')
> ['/home/lythanhphu/Movies/segment_5257520_1.ts', '/home/lythanhphu/Movies/segment_5257520_2.ts', '/home/lythanhphu/Movies/segment_5257520_3.ts', '/home/lythanhphu/Movies/segment_5257520_4.ts', '/home/lythanhphu/Movies/segment_5257520_5.ts', '/home/lythanhphu/Movies/segment_5257520_6.ts', '/home/lythanhphu/Movies/segment_5257520_7.ts', '/home/lythanhphu/Movies/segment_5257520_8.ts', '/home/lythanhphu/Movies/segment_5257520_9.ts', '/home/lythanhphu/Movies/segment_5257520_10.ts', '/home/lythanhphu/Movies/segment_5257520_11.ts', '/home/lythanhphu/Movies/segment_5257520_12.ts', '/home/lythanhphu/Movies/segment_5257520_13.ts']

There are many techniques you can use to download a file from an HTTP URL:


* The helper [function `urlretrieve`](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlretrieve) to download each individual video segment file. However, this function doesn't support an option to indicate a timeout to the HTTP request that is performed, meaning that if the request is blocked (for various possible reasons), your script could be blocked for ever. You could set the default timeout for new socket objects with the function, but this should be generally discouraged as it could introduce undesirable side effects in other parts of your application.

* The [function `urlopen`](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen) that supports the option `timeout`, which allows to specify a timeout in seconds for blocking operations like the connection attempt;

* The [third-party library `requests`](https://realpython.com/python-requests/), which [function `get`](https://2.python-requests.org/en/master/api/#requests.Request] also supports an option timeout.


*Note: how do we know how many video segments there are for an episode? We don't initially know this number. We could get this number by reading the M3U8 playlist of the episode; this probably the most generic solution, but it would be longer to implement. We suggest you to simply download video segments, incrementing the index of video segment for ever until your code catches a [HTTP 404 error "Not Found"](https://en.wikipedia.org/wiki/HTTP_404), meaning there is no more video segment.*

**Waypoint 8: Build the Final Video of an Episode

![video_editing.png]()

Write a `function build_episode_vide`o that takes two arguments `episode` and `segment_file_path_names` where:

* `episode`: An object `Episode`

* `segment_file_path_names`: a list of strings corresponding to absolute path and file names of TS video segments in the order of their index.

The function accepts an optional parameter `path` (a string) that indicates in with directory the episode's video file need to be saved into. If not defined, the function saves the episode video file in the path identified by the first video segment of the list `segment_file_path_names`.

The function assembles all these video segments in one video named after the identification of the episode.

The function returns the absolute path and file name of the episode's video.

For example:

>  Let's consider the following episode:
> >>> episode
> <__main__.Episode object at 0x1052b2eb8>
> >>> episode.title
> 'Trace'
> >>> episode.episode_id
> '5257520'
>  Download all the video segments of this episode in our directory
>  "Movies".
> >>> segment_file_path_names = download_episode_video_segments(episode, path='~/Movies')
>  Build the final video.
> >>> build_episode_video(episode, segment_file_path_names)
> '/home/lythanhphu/Movies/5257520.ts'

**Waypoint 9: Implement a Cache Strategy

You will need to run your script from time to time to download new episodes that TV5MONDE is going to publish. You don't want

However if you run the current version of your script, it downloads the video segments of every episode that it has previously downloaded. This results in a huge waste of time and an amazing useless CPU and network consumption.

You need to update your code to implement a caching mechanism, meaning that your code doesn't download again and again video segments that have been already downloaded.

**Waypoint 10: Support Downloading of Old Episodes

At this point, you might think you are finished to hack this TV5MONDE video program. Well, not totally.

Your script should work perfectly fine for almost all the episodes that have been published recently, minus some errors from TV5MONDE side. However, the current version of your script may no be able to download the videos of episodes that have been published in 2014.

The reason is that TV5MONDE doesn't use a M38U playlist to stream the video of these old episodes, but a single [MPEG-4](https://en.wikipedia.org/wiki/MPEG-4) video file per episode. If you closely inspect the broadcast data from the source code of an episode's Web page, you will notice that the format is not "`m3u8`" but "`mp4`", and the URL doesn't refer to a M38U playlist (that ultimately references other TS video segment files) but a MPEG-4 file.

You need to **elegantly** modify your script to support downloading the videos of these older episodes.

**Waypoint 11: Support Episodes with no Representative Image

Since the beginning of this mission, we have made the assumption that every episode has a representative image (cf. attribute image). And we use the URL of this representative image to extract the identification of the corresponding episode. Our code uses the identification of an episode is used to name the video segment files and the final video file of this episode.


**Problem

Unfortunately, we have discovered that a few episodes don't have representative image.

The current version of our code badly handles this situation. The static method `__parse_episode_id` of the class `Episode` that we have developed in the waypoint #2, returns an empty string as the identification of an episode with no representative image (or raises an exception). Without episode identification, our code cannot correctly saves the video segment files and the final video file of these episodes.

We could more surely retrieve the identification of the episode from the broadcast data of an episode, would this episode be split in several video segments or would this episode composed of only one MPEG-4 video file..

The problem with this solution is that it breaks our cache mechanism (cf. waypoint #9). Our cache mechanism allows our code to only fetch the list of episodes from TV5MONDE private API and to immediately detect which episodes has been already downloaded, which new episodes need to be downloaded. It's efficient. It's fast.

If we need to read the Web page of each episode and extract the broadcast data of this episode in order to retrieve the identification of this episode, and to decide whether we need to download or not the video files of this episode, our script would be very slow.

How can we fix this issue?Pragmatic Solution

**Pragmatic Solution

We can decide to generate a key to uniquely identify episodes. This key has to be generated from the data directly fetched from TV5MONDE private API, so no other request is required to take the decision whether we need to download the video files of an episode, or whether we need to skip this episode as we have already downloaded it.

An episode **always** has a dedicated Web page (cf. attribute `url`). This Web page is unique for each episode:

We can use this URL (actually a path) to generate a dedicated unique key for this episode. We will use the [MD5 message-digest algorithm](https://en.wikipedia.org/wiki/MD5) to produce a hash value of the episode's URL. We will use the [hexadecimal](https://en.wikipedia.org/wiki/Hexadecimal) representation of this hash to name the episode's video files.

For example, the path of the dedicated Web page of the episode "Tomate (et patate)" is "`/emissions/episode/merci-professeur-tomate-et-patate`". The [MD5](https://www.md5online.org/) hash value of this path is `caa8efbaaae3bb32cbd14a9ff6d73c63`.

We will replace in our code the way we name the video files of an episode, from the identification of the episode to this hash value.

You need to:

1. Add a private static method `__generate_key` to the class `Episode`, that takes an argument `s` (a string) and that returns a string representing the [MD5 hexadecimal hash value](https://docs.python.org/3/library/hashlib.html) of this argument `s`;

2. Update the constructor of the class `Episode` to create an additional private attribute and set its value with the hexadecimal hash value of the episode built from the URL (path only) of the Web page of the episode;

3. Add a read-only [property](https://www.programiz.com/python-programming/property) `key` to the class `Episode` that returns the unique key of the episode.

Then you need to refactor your code to name the video files of an episode with the key of this episode.





