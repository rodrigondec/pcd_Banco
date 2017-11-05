import socket
from pickle import dumps, loads
from configs.socket import HOST_N_PORT


class ClientConnection():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(HOST_N_PORT)

    def _send(self, data):
        data = dumps(data)
        self.socket.send(data)

    def _receive(self):
        data = self.socket.recv(1024)
        data = loads(data)
        return data

    def run(self):
        ack = self._receive()
        if not ack:
            raise Exception("ack falhou")
        print("recebido: {}".format(ack))

        operacao = "saldo"
        print("enviando: {}".format(operacao))
        self._send(operacao)

        done = self._receive()
        if not done:
            raise Exception("resposta falhou")
        print("recebido: {}".format(done))


if __name__ == "__main__":
    ClientConnection().run()
