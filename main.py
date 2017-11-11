from time import sleep
from subprocess import run
import sys
from sckt.SocketServer import SocketServer
from threading import _start_new_thread
from rmi.RMIServer import RMIServer, StartNameServer
from dominio.Pessoa import Pessoa, PessoaSocket, DependenteSocket


if __name__ == "__main__":
    _start_new_thread(StartNameServer, ("l_env/bin/activate",))
    sleep(3)
    # SocketServer().start()
    RMIServer().start()

    for _ in range(0, 2):

        PessoaSocket()
        DependenteSocket()

    Pessoa.start()
#
# from dominio.Banco import Banco
#
# from dominio.Pessoa import Pessoa, Dependente
#
# # VARIÁVEIS DE CONFIGURAÇÃO
# if len(sys.argv) != 4:
#     print("Número inválido de argumentos. Exatamente 3 argumentos requeridos, na seguinte ordem:" +
#         "\n1 - Número total de pessoas\n2 - Número toral de dependentes\n3 - Número total de caixas no banco")
#     os._exit(1)
#
# qt_pessoas = None
# qt_dependentes = None
#
# try:
#     qt_pessoas = int(sys.argv[1])
#     qt_dependentes = int(sys.argv[2])
#     Banco.qt_caixas = int(sys.argv[3])
# except ValueError:
#     print("Argumento(s) inválido(s)! Os 3 argumentos enviados necessitam ser do tipo inteiro")
#     os._exit(1)
#
# Banco()
#
# for _ in range(0, qt_pessoas):
#     Pessoa()
#
# for _ in range(0, qt_dependentes):
#     Dependente()
#
#
