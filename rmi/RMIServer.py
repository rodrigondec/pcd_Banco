import Pyro4
import os
from threading import _start_new_thread

from rmi.RMIServerBroker import RMIServerBroker

from config import HOST, RMI_PORT, RMI_NS_PORT



def StartNameServer(env):
    _start_new_thread(os.system, ("source {} & python -m Pyro4.naming -n {} -p {}".format(env, HOST, RMI_NS_PORT),))


class RMIServer():
    def __init__(self):
        self.daemon = Daemon()
        self.ns = locateNS(HOST, RMI_PORT)
        self.uri = self.daemon.register(Banco)
        self.ns.register("banco", self.uri)

    def start(self):
        print("RMI ready. Listening: {}:{}".format(self.uri, 1))      # print the uri so we can use it in the client later
        self.daemon.requestLoop()
