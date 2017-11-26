# Socket

## SocketServer

O servidor socket foi implementado utilizando a biblioteca nativa [Socket](https://docs.python.org/3/library/socket.html) do python. Ele recebe uma operação que foi serializada utilizando a biblioteca nativa [Pickle](https://docs.python.org/3/library/pickle.html) do python e depois manda a operação para ser executada no singleton do Banco, retornando o valor da execução da operação para o cliente.

### Código

```py
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
```

---

## SocketClientBroker

O cliente PessoaSocket e DependenteSocket utilizam a classe SocketClientBroker para realizar a comunicação com o servidor socket. E será nela que terá a conexão com o SocketServer, juntamente com a serialização da operação e desserialização da resposta.

### Código

```py
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
```



