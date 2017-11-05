#!/usr/bin/python3           # This is server.py file
import os
import sys
from pickle import dumps, loads
from models.Banco import Banco
# from configs import socket
import socket
from configs.socket import HOST_N_PORT
from threading import Thread, _start_new_thread
from time import sleep


class Server(Thread):
    def init(self):
        # create a socket object
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind to the port
        self.socket.bind(HOST_N_PORT)

        # queue up to 5 requests
        self.socket.listen(5)

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
        print("enviando ack...")
        self.send(client, True)

        operacao = self.receive(client)
        print("recebido: {}".format(operacao))
        sleep(3)

        print("enviando done...")
        self.send(client, True)

        client.close()

    def run(self):
        self.init()

        while True:
            # establish a connection
            print("Waiting connections...")
            client, addr = self.socket.accept()

            _start_new_thread(self.handler, (client, addr))


if __name__ == "__main__":
    # execute only if run as a script
    Server().start()
