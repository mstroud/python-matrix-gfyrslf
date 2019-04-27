import logging
import requests
import json
import urllib
import random
import re

import giphy_client
from giphy_client.rest import ApiException

from gfyrslf.command import GfyrslfCommand


class GifCommand(GfyrslfCommand):
    def __init__(self, cmdname, cfg):
        super().__init__(cmdname, cfg)
        self.description = "Requests an automatic random GIF post related to a specified query string"

        # Create an instance of the API class
        # TODO: Add to YAML config
        self.api_instance = giphy_client.DefaultApi()

        # Handle configuration
        self.limit = 1  # int | The maximum number of records to return. (optional) (default to 25)
        self.offset = 0  # int | An optional results offset. Defaults to 0. (optional) (default to 0)
        self.rating = 'R'  # str | Filters results by specified rating. (optional)
        self.lang = 'en'  # str | Specify default country for regional content; use a 2-letter ISO 639-1 country code. See list of supported languages <a href = \"../language-support\">here</a>. (optional)
        self.fmt = 'json'  # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

    def event_handler(self, bot, room, event):
        # Parse command args. TODO: Add helper function to parent class for arg parsing
        args = event['content']['body'].split()
        cmd = args.pop(0)
        match = re.search(self.regex, cmd)
        self.offset = 0 # Set default offset
        if match.group(1) is not None:
            if match.group(1) == 'r':
                self.offset = random.randrange(1, 42)
            else:
                self.offset = int(match.group(1))
                
        query = ' '.join(args)
        return self.event_handler_giphy(bot, room, query)
        #return self.event_handler_tenor(bot, room, query)

    def event_handler_giphy(self, bot, room, query):
        # Give the people a GIF
        try:
            # Search Giphy Endpoint
            api_response = self.api_instance.gifs_search_get(
                self.cfg['apis']['giphy']['api_key'],
                query,
                limit=self.limit,
                offset=self.offset,
                rating=self.rating,
                lang=self.lang,
                fmt=self.fmt)
            logging.debug(api_response)

        except ApiException as e:
            logging.warning("Exception when calling DefaultApi->gifs_search_get: {}\n".format(e))

        # Take the first hit and upload it to the Matrix server
        url = api_response.data[0].images.original.url
        response = requests.get(url, stream=False)
        mxc_url = bot.client.upload(response.content, response.headers['Content-Type'])

        # Send the media link to the room
        room.send_image(mxc_url, str(self.offset) + ' ' + api_response.data[0].slug + '(' + response.headers['Content-Type'] + ')',
                        mimetype=response.headers['Content-Type'])

    def event_handler_tenor(self, bot, room, query):
        # load the user's anonymous ID from cookies or some other disk storage
        # anon_id = <from db/cookies>

        # ELSE - first time user, grab and store their the anonymous ID
        r = requests.get("https://api.tenor.com/v1/anonid?key={}".format(self.cfg['apis']['tenor']['api_key']))

        if r.status_code == 200:
            anon_id = json.loads(r.content)["anon_id"]
            # store in db/cookies for re-use later
        else:
            anon_id = ""

        # get the top GIFs for the search term
        query_dict = {
            'q': query,
            'locale': 'en_US',
            'key': self.cfg['apis']['tenor']['api_key'],
            'limit':self.limit,
            'anon_id':anon_id,
            'contentfilter':'off',
            'media_filter':'minimal'
        }
        qs = urllib.parse.urlencode(query_dict)
        r = requests.get("https://api.tenor.com/v1/search?{}".format(qs))

        if r.status_code != 200:
            logging.warning("Status not OK: {}".format(r.status_code))
            return

        # Take the first hit and upload it to the Matrix server
        api_result = json.loads(r.content)['results'][0]

        url = api_result['media'][0]['gif']['url']
        slug = api_result['title'] + api_result['id']
        response = requests.get(url, stream=False)
        mxc_url = bot.client.upload(response.content, response.headers['Content-Type'])

        # Send the media link to the room
        room.send_image(mxc_url, slug + '(' + response.headers['Content-Type'] + ')',
                        mimetype=response.headers['Content-Type'])