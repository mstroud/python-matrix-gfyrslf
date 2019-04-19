import yaml
import logging
import traceback

from matrix_client.client import MatrixClient
from matrix_client.api import MatrixRequestError


class GfyrslfBot:
    def __init__(self, cfg='config.yml'):
        logging.debug("Opening config from: {}".format(cfg))
        with open(cfg, 'r') as cfgfile:
            self.cfg = yaml.load(cfgfile, Loader=yaml.Loader)

        # Add commands from config file
        self.commands = {}
        for cmdname in self.cfg['commands'].keys():
            self.add_command(cmdname)

        # Create client object and login to Matrix server
        self.client = MatrixClient(self.cfg['matrix']['server'])
        try:
            self.client.login(username=self.cfg['matrix']['username'],
                              password=self.cfg['matrix']['password'],
                              sync=True)
        except MatrixRequestError as e:
            logging.error(e)
            if e.code == 403:
                logging.error("Bad username/password")
        except Exception as e:
            logging.error("Invalid server URL: {}".format(e))
            traceback.print_exc()
            exit()

        # Automatically accept invites
        self.client.add_invite_listener(self.handle_invite)
        self.rooms = []

        # Add all rooms we're currently in to self.rooms and add their callbacks
        for room_id, room in self.client.rooms.items():
            room.add_listener(self.handle_message)
            self.rooms.append(room_id)

    def add_command(self, cmdname):
        # Add command modules
        cmdcfg = self.cfg['commands'][cmdname]
        module = str('gfyrslf.commands.' + cmdname)
        classname = cmdcfg['classname']
        logging.debug("Adding command class '{}' from module '{}'".format(classname, module))
        try:
            mod = __import__(module, fromlist=[classname])
            cls = getattr(mod, classname)
            inst = cls(cmdname,self.cfg)
            self.commands[cmdname] = inst
        except Exception as e:
            logging.error("Failed to load command classname '{}' from module '{}': {}".format(classname, module, e))
            traceback.print_exc()

    def handle_message(self, room, event):
        # Make sure we didn't send this message
        if event["sender"] == self.client.user_id:
            return
        
        # Check commands for matches
        logging.debug("Got non-self event from {} in {}".format(event["sender"],event["room_id"]))
        logging.debug(self.commands.values())
        for command in self.commands.values():
            if command.event_test(room, event):
                try:
                    command.event_handler(self, room, event)
                except:
                    traceback.print_exc()

    def handle_invite(self, room_id, state):
        logging.info("Got invite to room '{}', joining...".format(str(room_id)))
        room = self.client.join_room(room_id)

        # Add message callback for this room
        room.add_listener(self.handle_message)

        # Add room to list
        self.rooms.append(room)

        # Announce
        if self.cfg['bot']['announce'] is True:
            room.send_text(str("Howdy, I'm {}.\n" +
                               "Type '!{} help' to find out how to (ab)use me.").format(self.cfg['bot']['name'],
                                                                                        self.cfg['bot']['name']))

    def run(self):
        # Starts listening for messages
        self.client.start_listener_thread()
        return self.client.sync_thread


if __name__ == "__main__":
    import sys
    import time

    logging.basicConfig(level=logging.DEBUG)

    # Create an instance of GfyrslfBot
    gbot = GfyrslfBot(cfg='config.yml')

    # Start polling
    gbot.run()

    # Wait for exit
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            logging.info('Exiting...')
            sys.exit()