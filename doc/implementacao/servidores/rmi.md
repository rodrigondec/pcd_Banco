# RMI

# RMI NameServer

A bibliotera [Pyro4](https://pythonhosted.org/Pyro4/) disponibiliza um name server para que possa ser associada uma classe Exposed a uma string. No caso, a classe Exposed é a RMIServerBroker e a string é "banco" \(configuração feita no RMIServer\).

### Código

```py
def StartNameServer(env):
    _start_new_thread(os.system, ("source {} & python -m Pyro4.naming -n {} -p {}".format(env, HOST, RMI_NS_PORT),))
```

---

## RMIServerBroker

O RMIServerBroker possui nosso serviço oferecido por RMI, que é o realizar\_operação. Que recebe uma operação serializada com a biblioteca nativa [Pickle](https://docs.python.org/3/library/pickle.html) do python e retorna a resposta da operação serializada.

### Código

```py
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
```

---

## RMIServer

O servidor RMI foi implementado utilizando a biblioteca [Pyro4](https://pythonhosted.org/Pyro4/). Ele registra o RMIServerBroker no daemon do Pyro4 e no NameServer do Pyro4, e fica esperando requests.

### Código

```py
class RMIServer():
    def __init__(self):
        self.daemon = Pyro4.Daemon(host=HOST, port=RMI_PORT)
        self.ns = Pyro4.locateNS(HOST, RMI_NS_PORT)
        self.uri = self.daemon.register(RMIServerBroker())
        self.ns.register("banco", self.uri)

    def start(self):
        print("Banco RMI ready. Listening: {}".format(self.uri))      # print the uri so we can use it in the client later
        _start_new_thread(self.daemon.requestLoop, ())
```

---

## RMIClientBroker

O cliente PessoaRMI e DependenteRMI utilizam a classe RMIClientBroker para realizar a comunicação com o servidor RMI. E será nela que terá a conexão com o RMIServer, juntamente com a serialização da operação e desserialização da resposta.

### Código

```py
class RMIClientBroker:
    def __init__(self, operacao):
        self.operacao = operacao

    def execute(self):
        banco = Pyro4.Proxy("PYRONAME:banco")  # use name server object lookup uri shortcut
        data = dumps(self.operacao)

        resp = loads(tobytes(banco.realizar_operacao(data)))

        return resp
```



