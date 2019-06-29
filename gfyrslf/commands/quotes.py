import sqlite3
import logging
from gfyrslf.command import GfyrslfCommand

class QuoteCommand(GfyrslfCommand):
    
    def __init__(self,cmdname,cfg):
        super().__init__(cmdname,cfg)
        
    def event_handler(self, bot, room, event):
        self.db = sqlite3.connect(self.cfg['quotedb'])
        row = self.db.execute('SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1').fetchone() # TODO: try except? 
        self.db.close()
        logging.info("{} says ({}): '{}'".format(self.cfg['logname'],row[0],row[1]))
        room.send_text(row[1])
