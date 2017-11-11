from pickle import dumps, loads
import socket
from config import HOST, SOCKET_PORT
from threading import Thread, _start_new_thread

from dominio.Banco import Banco
from dominio.Exceptions import SaldoException


class SocketServer(Thread):
    def init(self):
        # create a socket object
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind to the port
        self.socket.bind((HOST, SOCKET_PORT))

        # queue up to 5 requests
        self.socket.listen(5)
        print("Socket ready. Listening: {}:{}".format(HOST, SOCKET_PORT))
        Banco()

    def send(self, client, data):
        data = dumps(data)
        client.send(data)

    def receive(self, client):
        # Receive no more than 1024 bytes
        data = client.recv(1024)
        data = loads(data)
        return data

    def handler(self, client, addr):
        ack = True
        resp = {}

        # print("enviando ack...")
        self.send(client, ack)

        operacao = self.receive(client)
        # print("recebido: {}".format(operacao))

        try:
            resp['status'] = True
            resp['msg'] = Banco().realizar_operacao(operacao)
        except SaldoException as e:
            resp['status'] = False
            resp['msg'] = e.message

        # print("enviando resposta...")
        # print(resp)
        self.send(client, resp)

        client.close()

    def run(self):
        self.init()

        while True:
            # print("Waiting connections...")
            client, addr = self.socket.accept()

            _start_new_thread(self.handler, (client, addr))
