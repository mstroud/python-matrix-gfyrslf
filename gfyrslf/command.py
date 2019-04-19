import logging
import re


class GfyrslfCommand(object):
    """Abstract class for commands
    often listing the methods you're expected to supply."""

    def __init__(self,cmdname,cfg):
        self.cmdname = cmdname
        self.description = "Default command"
        self.cfg = cfg['commands'][self.cmdname]

        # Check config for command_regex override
        if 'regex' in self.cfg.keys():
            self.regex = self.cfg['regex']
        else:
            # Check config for subcmd_regex override
            if 'subcmd_regex' in self.cfg.keys():
                self.subcmd_regex = self.cfg['subcmd_regex']

            # Assemble a default command string
            self.regex = cfg['bot']['cmd_prefix_regex'] + \
                         cfg['bot']['name'] + \
                         ' ' + \
                         self.subcmd_regex

    def event_handler(self, room, event):
        raise NotImplementedError("event_handler not implemented!")

    def event_test(self, room, event):
        if event['type'] == "m.room.message":
            if re.search(self.regex, event['content']['body']):
                # The message matches the regex, return true
                logging.info("GfyrslfCommand '{}' == '{}'?".format(self.regex, event['content']['body']))
                return True
        # No match, return False
        return False

    def get_help_html(self):
        return "<li><b>" + self.cmdname + "</b><ul>" + \
               "<li><u>Description:</u> " + self.description + "</li>" + \
               "<li><u>Command regex:</u> " + self.regex + "</li>" + \
               "</ul></li>"