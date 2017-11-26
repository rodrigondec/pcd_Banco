# PessoaRMI e DependenteRMI

## Descrição

bla

## Código

```py
class PessoaRMI(Pessoa):
    def __init__(self):
        Pessoa.__init__(self)

    def realizar_operacao(self, operacao):
        return RMIClientBroker(operacao).execute()


class DependenteRMI(Dependente):
    def __init__(self):
        Dependente.__init__(self)

    def realizar_operacao(self, operacao):
        return RMIClientBroker(operacao).execute()
```



