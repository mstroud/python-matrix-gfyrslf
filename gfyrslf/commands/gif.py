import logging
from gfyrslf.command import GfyrslfCommand
import requests

import giphy_client
from giphy_client.rest import ApiException


class GifCommand(GfyrslfCommand):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.command_regex = '^!gif'

        # Create an instance of the API class
        self.api_instance = giphy_client.DefaultApi()
        self.api_key = 'dc6zaTOxFJmzC'  # str | Giphy API Key.
        self.limit = 1  # int | The maximum number of records to return. (optional) (default to 25)
        self.offset = 0  # int | An optional results offset. Defaults to 0. (optional) (default to 0)
        self.rating = 'R'  # str | Filters results by specified rating. (optional)
        self.lang = 'en'  # str | Specify default country for regional content; use a 2-letter ISO 639-1 country code. See list of supported languages <a href = \"../language-support\">here</a>. (optional)
        self.fmt = 'json'  # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)


    def event_handler(self, bot, room, event):
        # Parse command args. TODO: Move to parent class
        args = event['content']['body'].split()
        args.pop(0)
        query = ' '.join(args)

        # Give the people a GIF
        try:
            # Search Giphy Endpoint
            api_response = self.api_instance.gifs_search_get(
                self.api_key,
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
        room.send_image(mxc_url, api_response.data[0].slug + '(' + response.headers['Content-Type'] + ')',
                        mimetype=response.headers['Content-Type'])
