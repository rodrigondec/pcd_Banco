from pickle import loads, dumps
from serpent import tobytes
import Pyro4


class RMIClientBroker:
    def __init__(self, operacao):
        self.operacao = operacao

    def execute(self):
        banco = Pyro4.Proxy("PYRONAME:banco")  # use name server object lookup uri shortcut
        data = dumps(self.operacao)

        resp = loads(tobytes(banco.realizar_operacao(data)))

        return resp
