import logging
import requests
import json
import urllib
import random
import re

from gfyrslf.command import GfyrslfCommand

"""
https://anapioficeandfire.com/Documentation
https://anapioficeandfire-python.readthedocs.io/en/latest/
"""

class ASOIAFWhoisCommand(GfyrslfCommand):
    def __init__(self, cmdname, cfg):
        super().__init__(cmdname, cfg)
        self.description = "Requests info about a character search query"

        # TODO: Everything

    def event_handler(self, bot, room, event):
        # Parse command args. TODO: Add helper function to parent class for arg parsing
        args = event['content']['body'].split()
        cmd = args.pop(0)
        match = re.search(self.regex, cmd)
        #return self.event_handler_tenor(bot, room, query)

    def event_handler_giphy(self, bot, room, query):
        #### # Give the people a GIF
        #### try:
        ####     # Search Giphy Endpoint
        ####     api_response = self.api_instance.gifs_search_get(
        ####         self.cfg['apis']['giphy']['api_key'],
        ####         query,
        ####         limit=self.limit,
        ####         offset=self.offset,
        ####         rating=self.rating,
        ####         lang=self.lang,
        ####         fmt=self.fmt)
        ####     logging.debug(api_response)
        #### 
        #### except ApiException as e:
        ####     logging.warning("Exception when calling DefaultApi->gifs_search_get: {}\n".format(e))
        #### 
        #### # Take the first hit and upload it to the Matrix server
        #### url = api_response.data[0].images.original.url
        #### response = requests.get(url, stream=False)
        #### mxc_url = bot.client.upload(response.content, response.headers['Content-Type'])
        #### 
        #### # Send the media link to the room
        #### room.send_image(mxc_url, str(self.offset) + ' ' + api_response.data[0].slug + '(' + response.headers['Content-Type'] + ')',
        ####                 mimetype=response.headers['Content-Type'])
        pass

    def event_handler_tenor(self, bot, room, query):
        #### # load the user's anonymous ID from cookies or some other disk storage
        #### # anon_id = <from db/cookies>
        #### 
        #### # ELSE - first time user, grab and store their the anonymous ID
        #### r = requests.get("https://api.tenor.com/v1/anonid?key={}".format(self.cfg['apis']['tenor']['api_key']))
        #### 
        #### if r.status_code == 200:
        ####     anon_id = json.loads(r.content)["anon_id"]
        ####     # store in db/cookies for re-use later
        #### else:
        ####     anon_id = ""
        #### 
        #### # get the top GIFs for the search term
        #### query_dict = {
        ####     'q': query,
        ####     'locale': 'en_US',
        ####     'key': self.cfg['apis']['tenor']['api_key'],
        ####     'limit':self.limit,
        ####     'anon_id':anon_id,
        ####     'contentfilter':'off',
        ####     'media_filter':'minimal'
        #### }
        #### qs = urllib.parse.urlencode(query_dict)
        #### r = requests.get("https://api.tenor.com/v1/search?{}".format(qs))
        #### 
        #### if r.status_code != 200:
        ####     logging.warning("Status not OK: {}".format(r.status_code))
        ####     return
        #### 
        #### # Take the first hit and upload it to the Matrix server
        #### api_result = json.loads(r.content)['results'][0]
        #### 
        #### url = api_result['media'][0]['gif']['url']
        #### slug = api_result['title'] + api_result['id']
        #### response = requests.get(url, stream=False)
        #### mxc_url = bot.client.upload(response.content, response.headers['Content-Type'])
        #### 
        #### # Send the media link to the room
        #### room.send_image(mxc_url, slug + '(' + response.headers['Content-Type'] + ')',
        ####                 mimetype=response.headers['Content-Type'])
        pass