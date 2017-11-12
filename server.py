from time import sleep

from sckt.SocketServer import SocketServer
from rmi.RMIServer import RMIServer, StartNameServer
from rest.RestServer import StartRestServer

from dominio.Banco import Banco


if __name__ == "__main__":
    Banco()
    StartNameServer("l_env/bin/activate")
    sleep(3)

    SocketServer().start()
    RMIServer().start()
    StartRestServer()
