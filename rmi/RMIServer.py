import Pyro4
import os
from threading import _start_new_thread

from rmi.RMIServerBroker import RMIServerBroker

from config import HOST, RMI_PORT, RMI_NS_PORT



def StartNameServer(env):
    _start_new_thread(os.system, ("source {} & python -m Pyro4.naming -n {} -p {}".format(env, HOST, RMI_NS_PORT),))


class RMIServer():
    def __init__(self):
        self.daemon = Pyro4.Daemon(host=HOST, port=RMI_PORT)
        self.ns = Pyro4.locateNS(HOST, RMI_NS_PORT)
        self.uri = self.daemon.register(RMIServerBroker())
        self.ns.register("banco", self.uri)

    def start(self):
        print("Banco RMI ready. Listening: {}".format(self.uri))      # print the uri so we can use it in the client later
        _start_new_thread(self.daemon.requestLoop, ())
