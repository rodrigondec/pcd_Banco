from time import sleep

from sckt.SocketServer import SocketServer
from rmi.RMIServer import RMIServer, StartNameServer

from dominio.Pessoa import Pessoa, PessoaSocket, DependenteSocket, PessoaRMI, DependenteRMI


if __name__ == "__main__":
    StartNameServer("l_env/bin/activate")
    sleep(3)

    SocketServer().start()
    RMIServer().start()

    for _ in range(0, 1):
        PessoaRMI()
        PessoaSocket()

        DependenteRMI()
        DependenteSocket()


    Pessoa.start()
