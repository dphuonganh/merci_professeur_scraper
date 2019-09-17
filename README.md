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
> # Download the video file "segment1_3_av.ts".
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
> # Display information about this file.
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

You **SHOULD** search for the hostname `hlstv5mplus-vh.akamaihd.net`. You will find it is included in a JSON expression similar to:

{
  "files": [
    {
      "format": "m3u8",
      "url": "https://hlstv5mplus-vh.akamaihd.net/i/hls/1b/4832469_,300,700,1400,2100,k.mp4.csmil/master.m3u8"
    }
  ],
  "primary": "html5",
  "token": false
}


