import socket
from pickle import dumps, loads
from config import HOST, SOCKET_PORT


class SocketClientBroker():
    def __init__(self, operacao):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((HOST, SOCKET_PORT))
        self._operacao = operacao

    def _send(self, data):
        data = dumps(data)
        self._socket.send(data)

    def _receive(self):
        data = self._socket.recv(2048)
        data = loads(data)
        return data

    def execute(self):
        ack = self._receive()
        if not ack:
            raise Exception("ack falhou")
        # print("recebido: {}".format(ack))

        # print("enviando: {}".format(self._operacao))
        self._send(self._operacao)

        return self._receive()
