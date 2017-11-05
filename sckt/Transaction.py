import socket
from pickle import dumps, loads
from configs.socket import HOST_N_PORT
from models.Pessoa import Pessoa


class Transaction():
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(HOST_N_PORT)
        self._call_before = False

    def _send(self, data):
        data = dumps(data)
        self._socket.send(data)

    def _receive(self):
        data = self._socket.recv(1024)
        data = loads(data)
        return data

    def before(self, operacao):
        self._operacao = operacao
        self._call_before = True

    def execute(self):
        if not self._call_before:
            return False
        ack = self._receive()
        if not ack:
            raise Exception("ack falhou")
        print("recebido: {}".format(ack))

        print("enviando: {}".format(self._operacao))
        self._send(self._operacao)

        done = self._receive()
        if not done:
            raise Exception("resposta falhou")

        print("recebido: {}".format(done))
        return done
