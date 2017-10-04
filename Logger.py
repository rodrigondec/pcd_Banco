from logging import getLogger, Formatter, FileHandler, StreamHandler, INFO
from time import strftime

class Log(object):
    @staticmethod
    def setup_logger(logger_name, log_file, level=INFO):
        l = getLogger(logger_name)
        formatter = Formatter('%(asctime)s;%(message)s', "%H:%M:%S")
        fileHandler = FileHandler(log_file, mode='w')
        fileHandler.setFormatter(formatter)
        streamHandler = StreamHandler()
        streamHandler.setFormatter(formatter)

        l.setLevel(level)
        l.addHandler(fileHandler)

    dir = "logs/"

    def __init__(self, nome):
        Log.setup_logger(nome, Log.dir+nome+".log")
        self.log =  getLogger(nome)

    def print(self, msg):
        print(str(strftime("%H:%M:%S"))+" "+msg)
        self.log.info(msg)
