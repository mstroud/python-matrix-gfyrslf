import logging
from gfyrslf.command import GfyrslfCommand

class HelloCommand(GfyrslfCommand):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.command_regex = '^!gfyrslf (hi|(he|hu)llo|howdy)'

    def event_handler(self, bot, room, event):
        logging.info(event)
        room.send_text("Hi, " + event['sender'])
