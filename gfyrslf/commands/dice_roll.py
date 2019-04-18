import random
import logging
from gfyrslf.command import GfyrslfCommand

class DiceCommand(GfyrslfCommand):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.command_regex = '^!gfyrslf d'

    def event_handler(self, bot, room, event):
        # someone wants a random number
        args = event['content']['body'].split()

        # we only care about the first arg, which has the die
        die = args[1]
        die_max = die[1:]

        # ensure the die is a positive integer
        if not die_max.isdigit():
            room.send_text('{} is not a positive number!'.format(die_max))
            return

        # and ensure it's a reasonable size, to prevent bot abuse
        die_max = int(die_max)
        if die_max <= 1 or die_max >= 1000:
            room.send_text('dice must be between 1 and 1000!')
            return

        # finally, send the result back
        result = random.randrange(1,die_max+1)
        logging.info("Dice roll random(1,{})=={}".format(die_max+1,result))
        room.send_text(str(result))