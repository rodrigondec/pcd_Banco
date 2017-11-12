from pickle import loads, dumps
from serpent import tobytes
from dominio.Banco import Banco
from dominio.Exceptions import SaldoException
import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class RMIServerBroker:
    def __init__(self):
        pass

    @staticmethod
    def realizar_operacao(data):
        operacao = loads(tobytes(data))

        resp = {}
        try:
            resp['status'] = True
            resp['msg'] = Banco().realizar_operacao(operacao)
        except SaldoException as e:
            resp['status'] = False
            resp['msg'] = e.message

        return dumps(resp)
