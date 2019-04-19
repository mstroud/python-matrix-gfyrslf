import logging
from gfyrslf.command import GfyrslfCommand

class HelloCommand(GfyrslfCommand):
    def __init__(self, cmdname, cfg):
        super().__init__(cmdname, cfg)
        self.description = "Replies \"Hi!\" to a variety of greetings"

    def event_handler(self, bot, room, event):
        room.send_text("Hi, " + event['sender'])
