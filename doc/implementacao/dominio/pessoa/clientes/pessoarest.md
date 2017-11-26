# PessoaRest e DependenteRest

## Descrição

bla

## Código

```py
class PessoaRest(Pessoa):
    def __init__(self):
        Pessoa.__init__(self)

    def realizar_operacao(self, operacao):
        return RestBroker(operacao).execute()


class DependenteRest(Dependente):
    def __init__(self):
        Dependente.__init__(self)

    def realizar_operacao(self, operacao):
        return RestBroker(operacao).execute()
```



