import logging
import re


class GfyrslfCommand(object):
    """Abstract class for commands
    often listing the methods you're expected to supply."""

    def __init__(self,cfg):
        pass

    def event_handler(self, room, event):
        raise NotImplementedError("event_handler not implemented!")

    def event_test(self, room, event):
        if event['type'] == "m.room.message":
            if re.search(self.command_regex, event['content']['body']):
                # The message matches the regex, return true
                logging.info("GfyrslfCommand '{}' == '{}'?".format(self.command_regex, event['content']['body']))
                return True
        # No match, return False
        return False