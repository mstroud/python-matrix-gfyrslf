import logging
from gfyrslf.command import GfyrslfCommand

class HelpCommand(GfyrslfCommand):
    def __init__(self, cmdname, cfg):
        super().__init__(cmdname, cfg)
        self.description = "Displays help information for various bot skills"

    def event_handler(self, bot, room, event):
        # Parse args for more info
        args = event['content']['body'].split()
        cmd = args[2] if len(args) > 2 else None

        # Check if a specific command help was requested
        if cmd is not None and cmd in bot.commands.keys():
            room.send_html(bot.commands[cmd].get_help_html())
        else:
            # Give the default help
            msg = "Here are all my tricks:\n"
            for cmd in bot.commands.values():
                msg = msg + cmd.get_help_html()
            room.send_html(msg)