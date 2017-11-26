# PessoaRest e DependenteRest

## Descrição

Nas implementação dos clientes Rest, são utilizados um RestClientBroker. Que recebe a operação,  e realiza o protocolo de comunicação com o Servidor Rest.

## Código

```py
class PessoaRest(Pessoa):
    def __init__(self):
        Pessoa.__init__(self)

    def realizar_operacao(self, operacao):
        return RestClientBroker(operacao).execute()


class DependenteRest(Dependente):
    def __init__(self):
        Dependente.__init__(self)

    def realizar_operacao(self, operacao):
        return RestClientBroker(operacao).execute()
```



