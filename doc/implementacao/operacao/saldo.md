# Descrição

O saldo é realizado em cima de uma conta. 

# Código

```
class Saldo(OperacaoUnary):
    """Operação de saldo"""
    def __init__(self, pessoa):
        OperacaoUnary.__init__(self, pessoa)
        self.conta = None

    def execute(self):
        if not self.call_before:
            return False

        valor = self.conta.saldo()

        self.after()

        return valor

    def after(self):
        return True

    def roll_back(self):
        pass
```



