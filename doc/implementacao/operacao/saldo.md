# Descrição

O saldo é realizado em cima de uma conta.

> OBS.: O lock da conta será adquirido apenas uma vez ao realizar o execute\(\) da operação. Já que a operação de saldo não é composta e sim simples \(atômica\)

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



