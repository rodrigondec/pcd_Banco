# PessoaSocket e DependenteSocket

## Descrição

Nas implementação dos clientes socket, são utilizados um SocketClientBroker. Que recebe a operação,  e realiza o protocolo de comunicação com o SocketServer.

## Código

```py
class PessoaSocket(Pessoa):
    def __init__(self):
        Pessoa.__init__(self)

    def realizar_operacao(self, operacao):
        return SocketClientBroker(operacao).execute()


class DependenteSocket(Dependente):
    def __init__(self):
        Dependente.__init__(self)

    def realizar_operacao(self, operacao):
        return SocketClientBroker(operacao).execute()
```



