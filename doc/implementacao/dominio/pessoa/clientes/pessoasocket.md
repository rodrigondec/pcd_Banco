# PessoaSocket e DependenteSocket

## Descrição

Na implementação dos clientes socket, são utilizados

## Código

```py
class PessoaSocket(Pessoa):
    def __init__(self):
        Pessoa.__init__(self)

    def realizar_operacao(self, operacao):
        return SocketBroker(operacao).execute()


class DependenteSocket(Dependente):
    def __init__(self):
        Dependente.__init__(self)

    def realizar_operacao(self, operacao):
        return SocketBroker(operacao).execute()
```



